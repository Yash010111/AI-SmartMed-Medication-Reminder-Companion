import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from pdf_handler import process_pdf
from chatgpt_api import BlackboxMedicationProcessor
from reminder import MedicationReminder
from PIL import Image, ImageTk


class MainApplication(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Medication Reminder App")
        self.master.geometry("1600x1080")
        
        # Load and set background image
        self.bg_image = Image.open("bg.jpg")
        self.bg_image = self.bg_image.resize((1600, 1080), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        
        # Create a canvas for the background image
        self.canvas = tk.Canvas(self.master, width=1600, height=1080)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        
        # Create a container frame for widgets
        self.container = tk.Frame(self.canvas, bg="white")
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        
        self.create_widgets()



    def create_widgets(self):
        # File Upload Section
        self.upload_frame = ttk.LabelFrame(self.container, text="Upload Prescription")

        self.upload_frame.pack(padx=10, pady=10, fill="x")
        
        self.upload_label = ttk.Label(self.upload_frame, text="Select PDF File:")
        self.upload_label.pack(side="left", padx=5)
        
        self.upload_button = ttk.Button(self.upload_frame, text="Browse", command=self.upload_pdf)
        self.upload_button.pack(side="right", padx=5)
        
        # Phone Number Entry
        self.phone_frame = ttk.LabelFrame(self.container, text="Enter WhatsApp Number")

        self.phone_frame.pack(padx=10, pady=10, fill="x")
        
        self.phone_label = ttk.Label(self.phone_frame, text="Phone Number (with country code):")
        self.phone_label.pack(side="left", padx=5)
        
        self.phone_entry = ttk.Entry(self.phone_frame)
        self.phone_entry.pack(side="right", padx=5, fill="x", expand=True)

        # Current Medications Section
        self.medications_frame = ttk.LabelFrame(self.container, text="Current Medications")

        self.medications_frame.pack(padx=10, pady=10, fill="x")
        
        self.medications_text = tk.Text(self.medications_frame, height=5)
        self.medications_text.pack(fill="x", padx=5, pady=5)
        
        # Next Alert Section
        self.alert_frame = ttk.LabelFrame(self.container, text="Next Alert")

        self.alert_frame.pack(padx=10, pady=10, fill="x")
        
        self.alert_label = ttk.Label(self.alert_frame, text="No upcoming alerts")
        self.alert_label.pack(padx=5, pady=5)
        
        # Reminders Section
        self.reminders_frame = ttk.LabelFrame(self.container, text="Medication Schedule")

        self.reminders_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.reminders_text = tk.Text(self.reminders_frame, height=10)
        self.reminders_text.pack(fill="both", expand=True, padx=5, pady=5)

    def upload_pdf(self):
        def process_in_thread():
            try:
                file_path = filedialog.askopenfilename(
                    filetypes=[("PDF Files", "*.pdf")]
                )
                if file_path:
                    # Process PDF
                    pdf_text = process_pdf(file_path)
                    
                    # Get medication schedule
                    processor = BlackboxMedicationProcessor()
                    schedule = processor.get_medication_schedule(pdf_text)
                    
                    if schedule:
                        # Verify we got 3 medications
                        if len(schedule) != 3:
                            messagebox.showerror("Error", f"Expected 3 medications, got {len(schedule)}")
                            return
                            
                        # Show medications in UI immediately
                        self.show_reminders(schedule)
                        
                        # Set up reminders
                        phone_number = self.phone_entry.get()
                        if not phone_number:
                            messagebox.showerror("Error", "Please enter a valid phone number")
                            return
                        
                        reminder = MedicationReminder(phone_number)
                        all_reminders = []
                        for med in schedule:
                            if med.strip():
                                parts = med.split("----")
                                if len(parts) == 3:
                                    medication, dosage, time = parts
                                    # Schedule reminder and get confirmation
                                    success = reminder.send_reminder(f"{medication} ({dosage})", time)
                                    if success:
                                        all_reminders.append(f"{medication} ({dosage}) at {time}")

                        # Show confirmation of scheduled reminders
                        if all_reminders:
                            messagebox.showinfo("Reminders Scheduled", 
                                "Successfully scheduled reminders for:\n" + 
                                "\n".join(all_reminders))

                    else:
                        messagebox.showerror("Error", "Could not process medication schedule")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
        # Run processing in a separate thread
        import threading
        threading.Thread(target=process_in_thread, daemon=True).start()

    def show_reminders(self, reminders):
        self.medications_text.delete(1.0, tk.END)
        self.reminders_text.delete(1.0, tk.END)
        
        # Extract unique medications and next alert time
        medications = set()
        next_alert = None
        all_times = []

        
        for reminder in reminders:
            if '----' in reminder:
                medication, dosage, times = reminder.split('----')
                medications.add(f"{medication} ({dosage})")
                
                # Find the next alert time
                times_list = times.split(',')
                for time in times_list:
                    try:
                        # Handle both time formats (HH:MM and text descriptions)
                        if ':' in time:
                            alert_time = datetime.strptime(time.strip(), "%H:%M").time()
                        else:
                            # Convert text descriptions to times
                            if 'morning' in time.lower():
                                alert_time = datetime.strptime("10:00", "%H:%M").time()
                            elif 'afternoon' in time.lower():
                                alert_time = datetime.strptime("15:00", "%H:%M").time()
                            elif 'evening' in time.lower():
                                alert_time = datetime.strptime("21:00", "%H:%M").time()
                            elif 'bedtime' in time.lower():
                                alert_time = datetime.strptime("21:00", "%H:%M").time()
                            else:
                                continue
                                
                        current_time = datetime.now().time()
                        if alert_time > current_time:
                            all_times.append(alert_time)
                            if next_alert is None or alert_time < next_alert:
                                next_alert = alert_time
                    except ValueError as e:
                        logger.debug(f"Error parsing time '{time}': {e}")
                        continue


                        
                self.reminders_text.insert(tk.END, f"{reminder}\n")
            
        # Display current medications
        self.medications_text.insert(tk.END, "\n".join(medications))
        
        # Display next alert
        if next_alert:
            self.alert_label.config(text=f"Next alert at {next_alert.strftime('%H:%M')}\n" +
                                  f"Total reminders scheduled: {len(all_times)}")
        else:
            self.alert_label.config(text="No upcoming alerts\nNo reminders scheduled")
