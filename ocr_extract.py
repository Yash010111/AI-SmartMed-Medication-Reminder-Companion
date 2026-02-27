import easyocr
from google import genai

GEMINI_API_KEY = "AIzaSyDte5Xqe4uKlDhhB_kRlg8pdAWRMC4s38E"

client = genai.Client(api_key=GEMINI_API_KEY)

def call_gemini_api(text, prompt):
    """
    Call Google Gemini API to transform the extracted text as needed for display.
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt + "\n\n" + text
        )
        transformed_text = response.text
        return transformed_text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return None

def extract_and_transform_prescription(image_path):
    # Initialize EasyOCR reader
    reader = easyocr.Reader(['en'])

    # Read text from image
    result = reader.readtext(image_path, detail=0, paragraph=True)
    text = "\n".join(result)

    # Print raw text (for debugging)
    print("Extracted Text:")
    print(text)

    # Define prompt for Gemini API to format the data for alert scheduling without patient details
    prompt = (
        "Format the following prescription text into a well-structured JSON object for alert scheduling. "
        "The JSON must have the following structure:\n"
        "{\n"
        "  \"medicines\": [\n"
        "    {\n"
        "      \"name\": \"string\",\n"
        "      \"dosage\": \"string\",\n"
        "      \"timing\": \"string\"  // explicit time in 24-hour format like '10:00', '14:00', '20:00'\n"
        "    }\n"
        "  ]\n"
        "}\n"
        "For medicines with dosage patterns like '1-0-1', return separate entries for each dose time (e.g., morning and night) with explicit timing strings in 24-hour format. "
        "If no specific time is given, use default times: 10:00 for morning, 14:00 for midday, and 20:00 for night. "
        "Ensure the JSON is properly formatted and ready for alert scheduling."
    )

    # Call Gemini API to transform the extracted text
    transformed_text = call_gemini_api(text, prompt)
    if transformed_text:
        print("\nTransformed Text from Gemini API:")
        print(transformed_text)
        # Strip markdown code block formatting if present
        if transformed_text.startswith("```") and transformed_text.endswith("```"):
            # Remove first line and last line
            lines = transformed_text.splitlines()
            if len(lines) > 2:
                transformed_text = "\n".join(lines[1:-1])
    else:
        print("\nFailed to transform text using Gemini API.")

    return transformed_text

if __name__ == "__main__":
    image_path = "precrip.jpg"
    extract_and_transform_prescription(image_path)
