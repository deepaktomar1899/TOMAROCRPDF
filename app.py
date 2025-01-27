from flask import Flask, render_template, request, jsonify
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import io
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        # Check if the file is a PDF
        if file.filename.endswith('.pdf'):
            text = convert_pdf_to_text(file)
            return jsonify({'text': text})

        # If the file is an image, try OCR
        elif file.filename.lower().endswith(('png', 'jpg', 'jpeg')):
            text = ocr_from_image(file)
            return jsonify({'text': text})

        return jsonify({'error': 'Invalid file format. Please upload a PDF or an image.'})
    
    return jsonify({'error': 'No file uploaded.'})

def convert_pdf_to_text(file):
    """Convert a PDF to text by first converting it to images and then performing OCR."""
    # Convert PDF to list of images
    images = convert_from_path(file, 300)  # 300 dpi for better quality
    
    text = ""
    for image in images:
        # Convert image to text using Tesseract OCR
        text += pytesseract.image_to_string(image, lang='eng+hin')  # Add 'hin' for Hindi OCR support
    
    return text

def ocr_from_image(file):
    """Extract text from an image using OCR."""
    image = Image.open(io.BytesIO(file.read()))
    text = pytesseract.image_to_string(image, lang='eng+hin')  # Add 'hin' for Hindi OCR support
    return text

if __name__ == '__main__':
    app.run(debug=True)
