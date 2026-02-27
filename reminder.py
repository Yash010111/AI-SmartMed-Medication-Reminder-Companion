from twilio.rest import Client
from datetime import datetime, timedelta
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Twilio credentials (replace with your actual credentials)
TWILIO_ACCOUNT_SID = "###########"
TWILIO_AUTH_TOKEN = "###########"
TWILIO_WHATSAPP_NUMBER = "###########"  # Twilio sandbox WhatsApp number or your WhatsApp-enabled Twilio number

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

import threading
import sqlite3

class MedicationReminder:
    def __init__(self, phone_number, db_path='app.db'):
        # Ensure phone number is in WhatsApp format
        if not phone_number.startswith("whatsapp:"):
            self.phone_number = f"whatsapp:{phone_number}"
        else:
            self.phone_number = phone_number
        self.db_path = db_path
        self.stop_event = threading.Event()

    def send_whatsapp_message(self, message_body):
        try:
            message = client.messages.create(
                from_=TWILIO_WHATSAPP_NUMBER,
                body=message_body,
                to=self.phone_number
            )
            logger.info(f"WhatsApp message sent to {self.phone_number}, SID: {message.sid}")
            return True
        except Exception as e:
            logger.error(f"Failed to send WhatsApp message: {e}")
            return False

    def check_and_send_due_reminders(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            now = datetime.now()
            current_time_str = now.strftime("%H:%M")
            # Fetch medications due at current time
            cursor.execute('SELECT name, dosage, timing FROM medications WHERE timing = ?', (current_time_str,))
            meds_due = cursor.fetchall()
            for med in meds_due:
                med_name = med[0]
                dosage = med[1]
                timing = med[2]
                message_body = f"🚨 *AI Meds Assistant* 🚨\n\nTIME TO TAKE YOUR MEDICINE!\n\n💊 Medication: {med_name}\n📏 Dosage: {dosage}\n⏰ Time: {timing}\n\nStay healthy! 💪"
                success = self.send_whatsapp_message(message_body)
                if success:
                    logger.info(f"Sent scheduled reminder for {med_name} at {timing}")
                else:
                    logger.error(f"Failed to send scheduled reminder for {med_name} at {timing}")
            conn.close()
        except Exception as e:
            logger.error(f"Error checking/sending reminders: {e}")

    def scheduler_loop(self):
        while not self.stop_event.is_set():
            self.check_and_send_due_reminders()
            # Sleep for 10 seconds before next check
            self.stop_event.wait(10)

    def start_scheduler(self):
        self.scheduler_thread = threading.Thread(target=self.scheduler_loop, daemon=True)
        self.scheduler_thread.start()

    def stop_scheduler(self):
        self.stop_event.set()
        self.scheduler_thread.join()
