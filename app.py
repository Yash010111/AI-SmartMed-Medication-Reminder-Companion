from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from pdf_handler import process_pdf

from reminder import MedicationReminder
import logging
from datetime import datetime
import json
import sqlite3
from flask import g
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from ocr_extract import extract_and_transform_prescription

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

DATABASE = 'app.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')
        # Add missing columns if they don't exist
        columns_to_add = {
            'name': 'TEXT',
            'age': 'TEXT',
            'gender': 'TEXT',
            'whatsapp': 'TEXT'
        }
        cursor.execute("PRAGMA table_info(users)")
        existing_columns = [row['name'] for row in cursor.fetchall()]
        for column, col_type in columns_to_add.items():
            if column not in existing_columns:
                cursor.execute(f"ALTER TABLE users ADD COLUMN {column} {col_type}")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                dosage TEXT NOT NULL,
                timing TEXT NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        db.commit()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if not username or not email or not password:
            flash('Please fill all fields', 'error')
            return redirect(url_for('signup'))
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute('INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                           (username, email, generate_password_hash(password)))
            db.commit()
            flash('Signup successful. Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username or email already exists.', 'error')
            return redirect(url_for('signup'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        if user and check_password_hash(user['password_hash'], password):
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login successful.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
        else:
            flash('Invalid username or password.', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user_id = session['user_id']
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        whatsapp = request.form.get('whatsapp')

        if not all([name, age, gender, whatsapp]):
            flash('Please fill all fields', 'error')
            return redirect(url_for('profile'))

        # Save profile data in users table
        cursor.execute('''
            UPDATE users SET name = ?, age = ?, gender = ?, whatsapp = ? WHERE id = ?
        ''', (name, age, gender, whatsapp, user_id))
        db.commit()

        profile_data = {
            'name': name,
            'age': age,
            'gender': gender,
            'whatsapp': whatsapp
        }
        success_message = "Profile saved successfully."
        return render_template('profile.html', profile=profile_data, success_message=success_message)

    # On GET, fetch profile data from database
    cursor.execute('SELECT name, age, gender, whatsapp FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    profile_data = {
        'name': user['name'],
        'age': user['age'],
        'gender': user['gender'],
        'whatsapp': user['whatsapp']
    }
    return render_template('profile.html', profile=profile_data)

@app.route('/dextop_alert')
@login_required
def manual_entry():
    user_id = session['user_id']
    db = get_db()
    cursor = db.cursor()

    # Fetch profile data from database (not session)
    cursor.execute('SELECT name, age, gender, whatsapp FROM users WHERE id = ?', (user_id,))
    profile_data = cursor.fetchone()
    if not profile_data or not profile_data['whatsapp']:
        flash('Please configure your profile first.', 'error')
        return redirect(url_for('profile'))

    # Fetch medications from database for user
    cursor.execute('SELECT name, dosage, timing, status FROM medications WHERE user_id = ?', (user_id,))
    meds = cursor.fetchall()
    formatted_meds = []
    for med in meds:
        formatted_meds.append({
            'medicine': med['name'],
            'dosage': med['dosage'],
            'time': med['timing'],
            'status': med['status']
        })

    # Start background scheduler for WhatsApp reminders
    phone_number = profile_data['whatsapp']
    reminder = MedicationReminder(phone_number)

    # Start scheduler thread if not already started
    if not hasattr(app, 'reminder_scheduler_started'):
        reminder.start_scheduler()
        app.reminder_scheduler_started = True

    return render_template('dextop_alert.html', medications=formatted_meds)

@app.route('/upload_prescription', methods=['POST'])
@login_required
def upload_prescription():
    user_id = session['user_id']
    file = request.files.get('file')

    if not file:
        return jsonify({
            "status": {
                "success": False,
                "message": "Image file is required",
                "error_code": "MISSING_FILE"
            },
            "data": None
        })

    file_path = f"temp/{file.filename}"
    file.save(file_path)

    logger.info(f"Received prescription image upload")

    try:
        extracted_json = extract_and_transform_prescription(file_path)
        if not extracted_json:
            raise ValueError("Failed to extract prescription data")

        # Check if extracted_json is valid JSON string
        import json
        try:
            data = json.loads(extracted_json)
        except json.JSONDecodeError as jde:
            raise ValueError(f"Invalid JSON from Gemini API: {jde}")

        medications = data.get('medicines', [])
        # Add status field to each medicine
        for med in medications:
            med['status'] = 'Scheduled'

        # Save medications to database for user
        db = get_db()
        cursor = db.cursor()
        # Delete existing medications for user
        cursor.execute('DELETE FROM medications WHERE user_id = ?', (user_id,))
        # Insert new medications
        for med in medications:
            cursor.execute('INSERT INTO medications (user_id, name, dosage, timing, status) VALUES (?, ?, ?, ?, ?)',
                           (user_id, med.get('name', ''), med.get('dosage', ''), med.get('timing', ''), med.get('status', 'Scheduled')))
        db.commit()

        return jsonify({
            "status": {
                "success": True,
                "message": "Prescription image processed"
            },
            "data": {
                "medications": medications
            }
        })
    except Exception as e:
        logger.error(f"Error processing prescription image: {e}")
        session['processing_log'] = f"Error processing prescription image: {str(e)}"
        return jsonify({
            "status": {
                "success": False,
                "message": str(e),
                "timestamp": datetime.now().isoformat(),
                "error_code": "PROCESSING_ERROR"
            },
            "data": None
        })

@app.route('/upload_prescription_image', methods=['POST'])
def upload_prescription_image():
    file = request.files.get('file')

    if not file:
        return jsonify({
            "status": {
                "success": False,
                "message": "Image file is required",
                "error_code": "MISSING_FILE"
            },
            "data": None
        })

    file_path = f"temp/{file.filename}"
    file.save(file_path)

    logger.info(f"Received prescription image upload")

    try:
        extracted_json = extract_and_transform_prescription(file_path)
        if not extracted_json:
            raise ValueError("Failed to extract prescription data")

        # Parse JSON string to dict
        import json
        data = json.loads(extracted_json)

        medications = data.get('medicines', [])
        # Add status field to each medicine
        for med in medications:
            med['status'] = 'Scheduled'

        session['medications'] = medications

        return jsonify({
            "status": {
                "success": True,
                "message": "Prescription image processed"
            },
            "data": {
                "medications": medications
            }
        })
    except Exception as e:
        logger.error(f"Error processing prescription image: {e}")
        session['processing_log'] = f"Error processing prescription image: {str(e)}"
        return jsonify({
            "status": {
                "success": False,
                "message": str(e),
                "timestamp": datetime.now().isoformat(),
                "error_code": "PROCESSING_ERROR"
            },
            "data": None
        })

@app.route('/add_medication', methods=['POST'])
def add_medication():
    medications = request.form.getlist('medication')
    dosages = request.form.getlist('dosage')
    times = request.form.getlist('time')

    if len(medications) == 0 or len(dosages) == 0 or len(times) == 0:
        return render_template('dextop_alert.html',
                               success_message="Please fill all required fields",
                               medications=get_manual_medications())

    try:
        success_count = 0
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('login'))

        db = get_db()
        cursor = db.cursor()

        for i in range(len(medications)):
            medication = medications[i]
            dosage = dosages[i]
            time = times[i]
            if medication and dosage and time:
                cursor.execute('INSERT INTO medications (user_id, name, dosage, timing, status) VALUES (?, ?, ?, ?, ?)',
                               (user_id, medication, dosage, time, 'Scheduled'))
                success_count += 1
        db.commit()

        if success_count > 0:
            medications_list = get_manual_medications()
            return render_template('dextop_alert.html',
                                   success_message=f"Successfully added {success_count} medication reminder(s)",
                                   medications=medications_list)
        else:
            raise Exception("No valid medication entries to add")

    except Exception as e:
        logger.error(f"Error adding medication: {e}")
        return render_template('dextop_alert.html',
                               success_message=f"Error: {str(e)}",
                               medications=get_manual_medications())

def get_manual_medications():
    user_id = session.get('user_id')
    if not user_id:
        return []
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT name as medicine, dosage, timing as time, status FROM medications WHERE user_id = ?', (user_id,))
    meds = cursor.fetchall()
    medications = []
    for med in meds:
        medications.append({
            'medicine': med['medicine'],
            'dosage': med['dosage'],
            'time': med['time'],
            'status': med['status']
        })
    return medications

@app.route('/delete_medication', methods=['POST'])
def delete_medication():
    medication = request.form.get('medicine')
    dosage = request.form.get('dosage')
    time = request.form.get('time')

    if not medication or not dosage or not time:
        return "Invalid request", 400

    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('DELETE FROM medications WHERE name = ? AND dosage = ? AND timing = ?', (medication, dosage, time))
        db.commit()

        from flask import redirect, url_for
        return redirect(url_for('manual_entry'))
    except Exception as e:
        logger.error(f"Error deleting medication: {e}")
        from flask import redirect, url_for
        return redirect(url_for('manual_entry'))

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

if __name__ == '__main__':
    print("Starting Flask app at http://127.0.0.1:5000/")
    app.run( debug=True)
