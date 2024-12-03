import os
import csv
from flask import Flask, request, render_template, send_from_directory
import struct

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'bin'}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'schema' not in request.files or 'data' not in request.files:
            return "No file part", 400
        
        schema_file = request.files['schema']
        data_file = request.files['data']

        if schema_file.filename == '' or data_file.filename == '':
            return 'No selected file', 400

        if schema_file and allowed_file(schema_file.filename) and data_file and allowed_file(data_file.filename):
            schema_path = os.path.join(app.config['UPLOAD_FOLDER'], schema_file.filename)
            data_path = os.path.join(app.config['UPLOAD_FOLDER'], data_file.filename)
            schema_file.save(schema_path)
            data_file.save(data_path)

            departments_data, all_students = process_files(schema_path, data_path)

            for dept, records in departments_data.items():
                generate_csv(dept, records)

            success_message = "Validation is successful, files are processed."
            return render_template('result.html', success_message=success_message, all_students=all_students)

    return render_template('frontend.html')



if __name__ == '__main__':
    app.run(debug=True)
