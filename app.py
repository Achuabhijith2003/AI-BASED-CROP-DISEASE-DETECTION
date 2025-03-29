from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
from core.test_plant import predict_diseases
from core.db_operation import get_the_treatment
app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'image' not in request.files:
            return jsonify({'error': 'No file part'})
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No selected file'})
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            print("file_uploaded", filepath)
            predictdseases = predict_diseases(filepath)
            tretment=get_the_treatment(predictdseases)
            print(f"Tratement of {predictdseases} is {tretment}")
            return jsonify({'result': predictdseases, 'treatment': tretment})  # Return the result
        else:
            return jsonify({'error': 'Invalid file type'})
    return jsonify({'error': 'Invalid request'}) #added for cases where the request is not POST.

@app.route('/')
def index():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)