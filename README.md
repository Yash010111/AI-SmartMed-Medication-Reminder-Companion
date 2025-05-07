# Medication Reminder App

This project is a Medication Reminder application built with Python and Tkinter. It processes prescription PDFs, extracts medication schedules using an AI API, and sends WhatsApp reminders for medication times.

## Features

- Upload prescription PDFs to extract medication information.
- Schedule WhatsApp reminders for medication times.
- User-friendly GUI built with Tkinter.
- Background image support.

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Place the background image `bg.jpg` in the project root directory.

3. Run the application:

```bash
python app.py
```

## Notes

- The project uses the `pywhatkit` library to send WhatsApp messages. Ensure you have a stable internet connection and WhatsApp Web logged in on your default browser.
- The background image path has been updated to a relative path for GitHub readiness.
- No API keys or confidential data are hardcoded in the project.
- Sensitive or environment-specific files are excluded via `.gitignore`.

## Contributing

Feel free to fork and submit pull requests.

## License

This project is open source and available under the MIT License.
