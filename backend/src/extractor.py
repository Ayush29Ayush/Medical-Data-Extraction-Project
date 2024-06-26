import os
from pdf2image import convert_from_path
import pytesseract
import utils
from dotenv import load_dotenv

from parser_prescription import PrescriptionParser
from parser_patient_details import PatientDetailsParser

# Load environment variables from .env file
load_dotenv()

# Get the base directory from .env file
BASE_DIR = os.getenv('BASE_DIR')

if not BASE_DIR:
    raise EnvironmentError("BASE_DIR is not set in the .env file")

POPPLER_PATH = r'C:\poppler-24.02.0\Library\bin'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract(file_path, file_format):
    full_path = os.path.join(BASE_DIR, file_path)

    print("Base Directory:", BASE_DIR)
    print("Relative Path:", file_path)
    print("Full Path:", full_path)

    if not os.path.exists(full_path):
        raise FileNotFoundError(f"The file {full_path} does not exist.")
    
    #! step 1: extracting text from pdf file
    try:
        # Extracting text from pdf file
        pages = convert_from_path(full_path, poppler_path=POPPLER_PATH)
    except Exception as e:
        raise Exception(f"Failed to convert PDF to images: {e}")
    
    document_text = ""
    
    # for page in pages:
    #     try:
    #         processed_image = utils.preprocess_image(page)
    #         text = pytesseract.image_to_string(processed_image, lang='eng')
    #         document_text += '\n' + text
    #     except Exception as e:
    #         raise Exception(f"Failed to process image with Tesseract: {e}")

    if len(pages)>0:
        page = pages[0]
        processed_image = utils.preprocess_image(page)
        text = pytesseract.image_to_string(processed_image, lang='eng')
        document_text = '\n' + text

    #! step 2: extract fields from text
    if file_format == 'prescription':
        extracted_data = PrescriptionParser(document_text).parse()
    elif file_format == 'patient_details':
        extracted_data = PatientDetailsParser(document_text).parse()
    else:
        raise Exception(f"Invalid document format: {file_format}")

    return extracted_data


if __name__ == '__main__':
    try:
        data = extract(r'backend\resources\patient_details\pd_2.pdf', 'prescription')
        print(data)
    except Exception as e:
        print(f"Error: {e}")
