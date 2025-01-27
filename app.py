from flask import Flask, request, render_template, jsonify
import pytesseract
from pdf2image import convert_from_path
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded!'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file!'}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Convert PDF to images and extract text
    text = ""
    try:
        images = convert_from_path(filepath)
        for image in images:
            text += pytesseract.image_to_string(image)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        os.remove(filepath)

    return jsonify({'text': text})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
