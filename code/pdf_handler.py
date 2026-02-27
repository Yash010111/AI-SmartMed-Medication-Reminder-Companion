import PyPDF2
import os

def process_pdf(file_path):
    """
    Process PDF file and extract text content with improved error handling
    """
    try:
        # Validate file exists and is a PDF
        if not os.path.exists(file_path):
            raise ValueError("File does not exist")
            
        if not file_path.lower().endswith('.pdf'):
            raise ValueError("File is not a PDF")
            
        # Check file size
        if os.path.getsize(file_path) == 0:
            raise ValueError("PDF file is empty")
            
        with open(file_path, 'rb') as pdf_file:
            # Validate PDF structure
            try:
                reader = PyPDF2.PdfReader(pdf_file)
                if not reader.pages:
                    raise ValueError("PDF contains no readable pages")
                    
                text = ""
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                        
                if not text.strip():
                    raise ValueError("No text could be extracted from PDF - file may be scanned or encrypted")
                
                # Clean and normalize the extracted text
                text = text.replace('\r', '').replace('\t', ' ')
                lines = [line.strip() for line in text.splitlines() if line.strip()]
                
                # Return the full text for processing by MedicationProcessor
                return '\n'.join(lines)
                
            except (PyPDF2.errors.PdfReadError, PyPDF2.errors.PdfStreamError) as e:
                raise ValueError(f"Invalid or corrupted PDF file: {str(e)}")
                
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        raise ValueError(f"Failed to process PDF: {str(e)}")
