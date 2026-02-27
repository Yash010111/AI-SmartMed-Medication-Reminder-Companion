# Development Setup Guide

## Prerequisites
- Python 3.10+
- pip or uv
- Git (optional)
- Virtual environment tools (venv, virtualenv, or conda)

## Local Development Setup

### 1. Clone/Download Repository
```bash
cd /path/to/med-companion
```

### 2. Create Virtual Environment
```bash
# Using venv
python -m venv venv

# Activate
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r code/requirements.txt
```

### 4. Configure API Keys
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your-api-key
TWILIO_ACCOUNT_SID=your-sid
TWILIO_AUTH_TOKEN=your-token
FLASK_SECRET_KEY=your-secret-key
```

### 5. Run Development Server
```bash
cd code
python app.py
```

The application will be available at: `http://127.0.0.1:5000`

## Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 code.app:app
```

### Using Docker (Coming Soon)
```bash
docker build -t med-companion .
docker run -p 5000:5000 med-companion
```

### Environment Variables for Production
```bash
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://user:password@localhost/med_companion
GEMINI_API_KEY=your-production-api-key
```

## Testing

Run tests:
```bash
pytest code/tests/ -v
```

Check code style:
```bash
flake8 code/
```

## Debugging

Enable debug logging:
```python
# In app.py
logging.basicConfig(level=logging.DEBUG)
```

View database:
```bash
sqlite3 app.db
sqlite> .tables
sqlite> SELECT * FROM users;
```

## Common Issues

### Issue: ImportError: No module named 'flask'
**Solution:** Run `pip install -r code/requirements.txt`

### Issue: Database locked
**Solution:** Delete `app.db` and restart the application

### Issue: Port 5000 already in use
**Solution:** Change port in `app.py`:
```python
app.run(port=5001, debug=True)
```
