import tkinter as tk
from gui import MainApplication
from chatgpt_api import BlackboxMedicationProcessor
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Test API call
    # processor = BlackboxMedicationProcessor()
    # test_text = "Paracetamol 500mg at 14:45 , Amoxicillin 500mg three times daily, Cetirizine 10mg at bedtime"
    # logger.debug("Testing API with sample text")
    # schedule = processor.get_medication_schedule(test_text)
    # logger.debug(f"API returned: {schedule}")
    
    # Start GUI
    root = tk.Tk()
    app = MainApplication(master=root)
    app.mainloop()
