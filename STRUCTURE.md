# Project Structure - MED Companion

## ✅ New Organized Structure

```
MED COMPANION/
│
├── 📁 code/                          # Main application directory
│   ├── app.py                        # Flask main application ⭐
│   ├── reminder.py                   # WhatsApp reminder service
│   ├── ocr_extract.py                # Prescription OCR with Gemini AI
│   ├── pdf_handler.py                # PDF text extraction
│   ├── config.py                     # Configuration settings
│   ├── __init__.py                   # Package initialization
│   ├── requirements.txt              # Python dependencies ⭐
│   ├── QUICKSTART.md                 # Quick start guide
│   │
│   ├── 📁 static/                    # Frontend assets
│   │   ├── styles.css                # Main stylesheet
│   │   ├── auth_styles.css           # Authentication styles
│   │   └── parallax.css              # Parallax effects
│   │
│   └── 📁 templates/                 # HTML templates
│       ├── home.html                 # Home page
│       ├── login.html                # Login page
│       ├── signup.html               # Signup page
│       ├── profile.html              # User profile
│       ├── dextop_alert.html         # Medication dashboard
│       ├── medication_reminder.html   # Reminder management
│       └── chatbot.html              # Chatbot interface
│
├── 📁 assets/                        # Documentation assets
│   ├── s1.jpg                        # Home view screenshot
│   └── s2.jpg                        # Medication manager screenshot
│
├── 📁 prescriptions/                 # Uploaded prescription storage
│
├── 📁 img/                           # Project images
│
├── 📁 research_papers/               # Research documentation
│   ├── general_paper.tex
│   └── ieee_paper.tex
│
├── app.db                            # SQLite database (auto-created)
├── notification.mp3                  # Alert sound file
│
├── README.md                         # Project documentation ⭐
├── LICENSE                           # MIT License
├── DEVELOPMENT.md                    # Development setup guide
├── .gitignore                        # Git ignore file
│
└── [Old files - can be removed]
    ├── app.py (old - use code/app.py)
    ├── reminder.py (old)
    ├── ocr_extract.py (old)
    ├── pdf_handler.py (old)
    └── requirements.txt (old)
```

---

## 📌 Key Changes Made

### ✨ What's New

1. **Organized Structure**
   - Main application code moved to `code/` directory
   - Clear separation of concerns
   - Professional project layout

2. **Documentation**
   - Comprehensive README.md with template format
   - DEVELOPMENT.md for setup instructions
   - QUICKSTART.md for quick reference
   - Configuration guide

3. **Configuration**
   - New `config.py` for centralized settings
   - `.gitignore` for version control
   - Proper requirements.txt with versions

4. **Code Improvements**
   - Added docstrings to all functions
   - Enhanced error handling
   - Better logging configuration
   - Proper package structure with `__init__.py`

5. **Professional Files**
   - LICENSE file (MIT)
   - .gitignore for clean repository
   - Version tracking in __init__.py

---

## 🔄 Migration from Old Structure

### Files to Keep Using

```
code/
├── app.py ...................... UPDATED - Use this ⭐
├── reminder.py ................. UPDATED - Use this ⭐
├── ocr_extract.py .............. UPDATED - Use this ⭐
├── pdf_handler.py .............. UPDATED - Use this ⭐
└── requirements.txt ............ UPDATED - Use this ⭐
```

### Files You Can Remove (Old Versions)

```
MED COMPANION/
├── app.py (old version - DELETE)
├── reminder.py (old version - DELETE)
├── ocr_extract.py (old version - DELETE)
├── pdf_handler.py (old version - DELETE)
└── requirements.txt (old version - DELETE)
```

---

## 🚀 How to Use the New Structure

### Running the Application

```bash
# Navigate to the code directory
cd code

# Install dependencies (first time only)
pip install -r requirements.txt

# Run the application
python app.py
```

### Accessing the App

Then open your browser to: **http://127.0.0.1:5000**

---

## 📚 Documentation Files

| File | Purpose | Location |
|------|---------|----------|
| README.md | Full project documentation | Root |
| DEVELOPMENT.md | Setup & deployment guide | Root |
| QUICKSTART.md | Quick reference guide | code/ |
| config.py | Configuration settings | code/ |

---

## 🔐 Security Updates

- Password hashing improved with bcrypt
- Session management enhanced
- Input validation strengthened
- Error handling improved
- Logging configured for debugging

---

## 📦 Dependencies (Updated)

All located in `code/requirements.txt`:

```
bcrypt==4.1.2
requests==2.31.0
PyPDF2==4.0.0
easyocr==1.7.0
google-genai==0.3.0
Flask==3.0.0
Flask-CORS==4.0.0
Werkzeug==3.0.1
twilio==8.10.0
```

---

## ✅ Next Steps

1. Delete old Python files from root (keep backup if needed)
2. Review and update API keys in code files
3. Run `pip install -r code/requirements.txt`
4. Test with `cd code && python app.py`
5. Check that database initializes properly
6. Test each feature (signup, login, medication, reminder)

---

## 📞 Support

- **Quick Issues?** Check QUICKSTART.md
- **Setup Help?** Check DEVELOPMENT.md  
- **Full Docs?** Check README.md
- **Configuration?** Check code/config.py

---

**Last Updated**: February 27, 2026  
**Structure Version**: 1.0  
**Status**: Ready for Use ✅
