import os
import glob
from flask import Flask

app = Flask(__name__)

# Absolute path to the folder containing the PDF files
DATA_FOLDER = r"E:\ELP\INNOFEM\data_files"

@app.route('/process')
def process_files():
    """Reads all PDF files in the folder, extracts text, processes it, and returns results."""
    
    # Get all PDF files in the directory
    files = glob.glob(os.path.join(DATA_FOLDER, "*.pdf"))
    results = []

    for file_path in files:
        # Extract text from the PDF file
        text = extract_text_from_pdf(file_path)
        
        if text:  # If text extraction is successful
            processed = compute_data(text)  # Process content
            results.append(f"{os.path.basename(file_path)}: {processed}")

    return "<br>".join(results) if results else "No PDFs found or no data extracted."

def extract_text_from_pdf(file_path):
    """Extract text from a PDF file using PyPDF2."""
    from PyPDF2 import PdfReader

    try:
        reader = PdfReader(file_path)
        text = ""  
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()  # Remove unnecessary spaces
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None  # Return None if extraction fails

def compute_data(content):
    """Processes extracted text and sums all numbers found in the content."""
    
    # Extract all numbers from the content
    numbers = [int(x) for x in content.split() if x.isdigit()]
    return sum(numbers)  # Return the sum of extracted numbers

if __name__ == '___main___':
    app.run(debug=True)