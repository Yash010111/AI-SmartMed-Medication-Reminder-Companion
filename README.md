# MED Companion

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Twilio API](https://img.shields.io/badge/Twilio-WhatsApp-orange.svg)](https://www.twilio.com/)
[![Google Gemini](https://img.shields.io/badge/Google-Gemini%20AI-blue.svg)](https://ai.google.dev/)

## 📋 Project Description

**MED Companion** is an intelligent medication reminder application that helps users manage their prescriptions through OCR-based prescription scanning, AI-powered medication extraction, and automated WhatsApp reminders. It is designed for personal health management and authorized medical tracking purposes.

### Key Functionalities
- **User Authentication** - Secure signup/login with password hashing
- **Prescription OCR** - Extract medications from prescription images using EasyOCR
- **AI Processing** - Parse prescription data using Google Gemini API
- **Medication Management** - Add, track, and manage medication schedules
- **Automated Reminders** - Send WhatsApp notifications at scheduled medication times
- **User Profiles** - Store and manage personal and health information
- **PDF Processing** - Extract and process medication data from PDF files
- **Medication Chatbot** - Interactive assistant for medication queries

---

## 🛠 Quick Start

Minimal commands to run locally:

```bash
pip install -r code/requirements.txt
cd code
python app.py
```

Open: http://127.0.0.1:5000

---

## 🖼 Screenshots

### Home / Dashboard View
![Home view](assets/s1.jpg)

### Medication Management Interface
![Medication Manager](assets/s2.jpg)

---

## 📁 Project Structure

```
code/
  ├─ app.py                    # Main Flask application
  ├─ reminder.py               # WhatsApp reminder service
  ├─ ocr_extract.py            # Prescription OCR & AI processing
  ├─ pdf_handler.py            # PDF text extraction
  ├─ requirements.txt          # Python dependencies
  ├─ static/                   # CSS stylesheets
  │  ├─ styles.css
  │  ├─ auth_styles.css
  │  └─ parallax.css
  └─ templates/                # HTML templates
     ├─ home.html
     ├─ login.html
     ├─ signup.html
     ├─ profile.html
     ├─ dextop_alert.html
     ├─ medication_reminder.html
     └─ chatbot.html

assets/
  ├─ s1.jpg                    # Home view screenshot
  └─ s2.jpg                    # Medication manager screenshot

README.md
LICENSE
```

---

## 🔧 Installation & Setup

### Prerequisites
- Python 3.10+
- pip or uv package manager
- Twilio account with WhatsApp enabled (optional)
- Google Gemini API key (obtain from [Google AI Studio](https://aistudio.google.com/apikey))

### Step-by-Step Installation

1. **Clone or download the repository**
   ```bash
   cd e:\Projects\MED COMPANION
   ```

2. **Install dependencies**
   ```bash
   pip install -r code/requirements.txt
   ```
   
   Or with `uv` (faster):
   ```bash
   uv pip install -r code/requirements.txt
   ```

3. **Configure API Keys**
   - Add your Google Gemini API key in `code/ocr_extract.py`
   - Add Twilio credentials in `code/reminder.py`

4. **Initialize Database**
   The database (`app.db`) is automatically created on first run.

5. **Run the Application**
   ```bash
   cd code
   python app.py
   ```

6. **Access the Application**
   Open your browser and navigate to: `http://127.0.0.1:5000`

---

## 📚 Core Features

### 1. User Authentication
- Secure account creation with email verification
- Password hashing using bcrypt
- Session-based authentication

### 2. Prescription Processing
- Upload prescription images (JPG, PNG)
- Automatic text extraction using EasyOCR
- AI-powered medication parsing with Google Gemini
- Structured JSON extraction with medicine name, dosage, and timing

### 3. Medication Management
- Add medications manually or via prescription upload
- Store dosage and timing information
- Track medication status
- Delete/update medication records

### 4. WhatsApp Reminders
- Scheduled medication reminders via WhatsApp
- Powered by Twilio API
- Automated background scheduler
- Real-time notification delivery

### 5. User Profile Management
- Store personal information (age, gender, contact)
- WhatsApp number for notifications
- Health profile tracking

---

## 🚀 API Endpoints

| Route | Method | Authentication | Description |
|-------|--------|-----------------|-------------|
| `/` | GET | None | Home page |
| `/signup` | GET, POST | None | User registration |
| `/login` | GET, POST | None | User login |
| `/logout` | GET | Yes | User logout |
| `/profile` | GET, POST | Yes | View/update user profile |
| `/dextop_alert` | GET | Yes | Medication dashboard |
| `/upload_prescription` | POST | Yes | Upload prescription image |
| `/upload_prescription_image` | POST | No | Upload without auth |
| `/add_medication` | POST | Yes | Add medication manually |
| `/delete_medication` | POST | Yes | Delete medication |
| `/chatbot` | GET | None | Medication chatbot |

---

## 🔐 Security Features

- **Password Hashing**: Bcrypt for secure password storage
- **Session Management**: Flask session with secure cookies
- **Input Validation**: Form validation and error handling
- **Database Security**: SQLite with parameterized queries to prevent SQL injection
- **API Key Protection**: Sensitive credentials stored in environment variables

### Security Best Practices

- Never run in production with `debug=True`
- Use environment variables for API keys
- Implement HTTPS/SSL in production
- Use a proper WSGI server (Gunicorn, uWSGI)
- Add rate limiting and CSRF protection

---

## 🛠 Configuration

### Environment Variables (Recommended)
```env
GEMINI_API_KEY=your-gemini-api-key
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
SECRET_KEY=your-flask-secret-key
DATABASE_URL=sqlite:///app.db
```

### Key Settings in `code/app.py`
```python
app.secret_key = 'your-secret-key-here'  # Change in production
DATABASE = 'app.db'  # SQLite database path
```

---

## 📖 Usage Examples

### Add Medication Manually
1. Log in to your account
2. Navigate to Dashboard
3. Click "Add Medication"
4. Fill in medication name, dosage, and timing
5. Save the medication

### Upload Prescription Image
1. Log in to your account
2. Click "Upload Prescription"
3. Select a prescription image
4. System automatically extracts medications
5. Review and confirm the extracted data

### Receive WhatsApp Reminders
1. Update your WhatsApp number in Profile
2. Add medications with specific times
3. Reminders will be sent via WhatsApp at scheduled times

---

## 🐛 Troubleshooting

### Issue: OCR not extracting text properly
**Solution:**
- Ensure prescription image is clear and well-lit
- Try with different image formats (JPG, PNG)
- Check EasyOCR language settings
- Verify Gemini API key is valid

### Issue: WhatsApp reminders not working
**Solution:**
- Verify Twilio credentials in `reminder.py`
- Check WhatsApp number format (include country code)
- Ensure Twilio WhatsApp sandbox is active
- Check application logs for error messages
- Verify internet connection

### Issue: Database errors
**Solution:**
- Delete `app.db` to reset database
- Check file permissions in project directory
- Ensure SQLite3 is properly installed

### Issue: API key errors
**Solution:**
- Verify Gemini API key is active
- Check API quota and usage limits
- Regenerate API key if needed
- Test API connectivity

---

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    name TEXT,
    age TEXT,
    gender TEXT,
    whatsapp TEXT
)
```

### Medications Table
```sql
CREATE TABLE medications (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    dosage TEXT NOT NULL,
    timing TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
```

---

## 📚 References

- [OWASP Web Security](https://owasp.org/www-project-top-ten/) - Web application security best practices
- [Flask Documentation](https://flask.palletsprojects.com/) - Flask framework reference
- [Google Gemini API](https://ai.google.dev/docs) - Gemini AI documentation
- [Twilio WhatsApp API](https://www.twilio.com/docs/whatsapp) - WhatsApp integration
- [EasyOCR Documentation](https://github.com/JaidedAI/EasyOCR) - OCR library
- [PyPDF2 Documentation](https://pypdf2.readthedocs.io/) - PDF processing

---

## 🏗 Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.10+ | Core Language |
| **Flask** | 3.0+ | Web Framework |
| **SQLite** | 3.x | Database |
| **Bcrypt** | 4.1+ | Password Hashing |
| **EasyOCR** | 1.7+ | Optical Character Recognition |
| **Google Gemini** | 2.0-flash | AI Text Processing |
| **Twilio** | 8.10+ | WhatsApp Integration |
| **PyPDF2** | 4.0+ | PDF Processing |
| **HTML/CSS/JS** | - | Frontend |

---

## 👥 Authors & Contact

- **Developer** — Yash Paraskar
- **Email** — yashparaskar2@gmail.com
- **GitHub** — https://github.com/Yash010111
- **LinkedIn** — https://www.linkedin.com/in/yash-paraskar-97a873271/
- **Issues / Support** — Create an issue in the repository

---

## 📄 License

This project is provided as-is for personal use and educational purposes. See [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Contributing

Contributions are welcome! To contribute:

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/med-companion.git
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/new-feature
   ```

3. **Make your changes** and test thoroughly

4. **Follow existing code style** and conventions
   - Add docstrings to functions
   - Use meaningful variable names
   - Keep functions modular and focused
   - Add error handling

5. **Test your changes**
   ```bash
   python -m pytest code/tests/ -v
   ```

6. **Update documentation** if adding new features

7. **Submit a pull request** with a clear description

### Development Guidelines

- Maintain code readability and consistency
- Add docstrings to all functions and classes
- Test changes on multiple prescription formats
- Ensure no hardcoded API keys or credentials
- Handle exceptions gracefully
- Follow Flask and Python best practices
- Add logging for debugging
- Use type hints where applicable

### Code Style
```python
# Good
def send_medication_reminder(user_id: int, medication: dict) -> bool:
    """Send WhatsApp reminder for medication"""
    try:
        # Implementation
        return True
    except Exception as e:
        logger.error(f"Error sending reminder: {e}")
        return False

# Avoid
def send_med_rem(id, med):
    try:
        # Implementation
    except:
        pass
```

---

## ⚠️ Disclaimer & Privacy

**This tool is provided for personal health management purposes only.**

- **Not a substitute for medical advice** - Always consult qualified healthcare professionals
- **Privacy & Data** - User data is stored locally in SQLite database
- **Responsible Use** - Use only with accurate prescription information
- **API Compliance** - Ensure compliance with Google Gemini and Twilio terms of service
- **Data Protection** - Implement additional security measures for production use

---

## 🔒 Security Disclaimer

**Please note the following important security considerations:**

- **Local Development Only** - Current setup uses Flask development server
- **For Production** - Use Gunicorn, uWSGI, or nginx for deployment
- **SSL/TLS** - Enable HTTPS in production environments
- **Database Backups** - Implement regular backup procedures
- **API Keys** - Never commit API keys; use environment variables
- **Access Control** - Implement additional authentication layers if needed

---

## 📈 Roadmap

Future enhancements under consideration:

- [ ] Mobile app (iOS/Android)
- [ ] Multi-language support
- [ ] Enhanced AI prescription parsing
- [ ] Email notifications
- [ ] SMS reminders
- [ ] Integration with medical APIs
- [ ] Unit test suite
- [ ] Docker containerization
- [ ] Cloud deployment guides
- [ ] Advanced analytics dashboard

---

## 📞 Support

For issues, questions, or feature requests:
1. Check existing GitHub issues
2. Review troubleshooting section above
3. Create a detailed issue with:
   - Error message/screenshot
   - Steps to reproduce
   - Your environment (OS, Python version)
   - Application logs

---

**Last Updated**: February 27, 2026  
**Developed for**: Personal Health Management & Medication Tracking  
**Status**: Active Development
