# MED Companion - Configuration

# Flask Configuration
DEBUG = False
TESTING = False
LOG_LEVEL = 'INFO'

# Database Configuration
DATABASE = 'app.db'
DATABASE_TIMEOUT = 5.0

# Session Configuration
PERMANENT_SESSION_LIFETIME = 86400  # 24 hours
SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# File Upload Configuration
UPLOAD_FOLDER = 'temp'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'pdf'}

# API Configuration
GEMINI_MODEL = 'gemini-2.0-flash'
OCR_LANGUAGE = ['en']

# Reminder Configuration
REMINDER_CHECK_INTERVAL = 10  # seconds
REMINDER_TIMEZONE = 'UTC'  # Change to your timezone

# Twilio Configuration (load from environment in production)
TWILIO_SANDBOX_MODE = True  # Set to False for production

# Security Configuration
SECRET_KEY = 'your-secret-key-here'  # CHANGE THIS IN PRODUCTION
BCRYPT_LOG_ROUNDS = 12  # Password hashing rounds
