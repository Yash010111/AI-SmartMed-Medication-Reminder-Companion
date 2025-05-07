import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)



class BlackboxMedicationProcessor:
    def __init__(self):
        self.url = "https://api.blackbox.ai/api/chat"
        self.headers = {'Content-Type': 'application/json'}
        self.system_prompt = """
        You are a medical assistant. Extract medication information from the provided text.
        Return the data in this format:
        [medication_name]----[dosage]----[time]
        If time is not specified, use default times:
        - Morning: 10:00
        - Afternoon: 15:00
        - Evening: 21:00
        """

    def get_medication_schedule(self, text):
        """
        Process text to extract medication schedule with improved error handling
        """
        try:
            # Validate input text
            if not text or not isinstance(text, str):
                raise ValueError("Invalid input text")
                
            # Prepare API request
            payload = {
                "messages": [
                    {
                        "content": self.system_prompt + "\n" + text,
                        "role": "user"
                    }
                ],
                "model": "deepseek-ai/DeepSeek-V3",
                "max_tokens": 1024
            }

            
            # Make API request
            logger.debug(f"Sending API request with payload: {payload}")
            response = requests.post(self.url, headers=self.headers, json=payload, timeout=10)
            logger.debug(f"Received API response: {response.status_code} - {response.text}")




            response.raise_for_status()  # Raise exception for HTTP errors
            
            # Parse response text
            response_text = response.text.strip()
            
            # Extract medication data from response
            if "Here is the extracted medication information" in response_text:
                # Extract the medication list after the header
                content = "\n".join(response_text.split("\n")[1:])
            else:
                content = response_text



                
            # Validate medication data
            if not content:
                raise ValueError("No medication data found in response")

                
            # Split and validate medication entries
            medications = content.split('\n')
            valid_medications = []
            for med in medications:
                med = med.strip()
                if med:
                    # Handle both [time1, time2] and single time formats
                    if '----' in med:
                        parts = med.split('----')
                        if len(parts) == 3:
                            # Clean up time format if needed
                            medication, dosage, time = parts
                            time = time.replace('[', '').replace(']', '')
                            valid_medications.append(f"{medication}----{dosage}----{time}")

                        
            if not valid_medications:
                raise ValueError("No valid medication entries found")
                
            logger.debug(f"Extracted medications: {valid_medications}")
            return valid_medications

            
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return None
        except (ValueError, KeyError) as e:
            print(f"Error processing medication data: {e}")
            return None
