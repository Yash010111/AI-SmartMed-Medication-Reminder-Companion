import pywhatkit as kit
from datetime import datetime
import time

class MedicationReminder:
    def __init__(self, phone_number):
        self.phone_number = phone_number

    def send_reminder(self, medication, time):
        """
        Send a medication reminder via WhatsApp with enhanced formatting
        """
        try:
            # Handle multiple times separated by commas
            times = [t.strip() for t in time.split(',')]
            
            for t in times:
                try:
                    reminder_time = datetime.strptime(t, "%H:%M")
                    
                    # Extract medication details
                    med_name = medication.split('(')[0].strip()
                    dosage = medication.split('(')[1].split(')')[0].strip()
                    
                    # Create formatted message
                    message = (
                        "🚨 *AI Meds Assistant* 🚨\n\n"
                        "TIME TO TAKE YOUR MEDICINE!\n\n"
                        f"💊 *Medication*: {med_name}\n"
                        f"📏 *Dosage*: {dosage}\n"
                        f"⏰ *Time*: {t}\n\n"
                        "Stay healthy! 💪"
                    )
                    
                    # Send message at scheduled time
                    kit.sendwhatmsg(
                        phone_no=self.phone_number,
                        message=message,
                        time_hour=reminder_time.hour,
                        time_min=reminder_time.minute,
                        wait_time=5,

                        tab_close=True
                    )




                except ValueError as e:
                    print(f"Error parsing time '{t}': {e}")
                    continue
            return True

        except Exception as e:
            print(f"Error sending reminder: {e}")
            return False
