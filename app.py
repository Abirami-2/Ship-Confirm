from flask import Flask, render_template, request, jsonify
import xml.etree.ElementTree as ET
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def find_duplicates(xml_content):
    tree = ET.ElementTree(ET.fromstring(xml_content))
    root = tree.getroot()
    hu_elements = [hu.attrib for hu in root.findall('.//HU')]
    seen = set()
    duplicates = set()
    for hu in hu_elements:
        hu_id = hu.get('id')
        if hu_id in seen:
            duplicates.add(hu_id)
        else:
            seen.add(hu_id)
    return list(duplicates)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        with open(os.path.join(app.config['UPLOAD_FOLDER'], file.filename), 'r') as f:
            xml_content = f.read()
        duplicates = find_duplicates(xml_content)
        return jsonify({'duplicates': duplicates})

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
