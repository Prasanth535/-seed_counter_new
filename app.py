import os
from flask import Flask, render_template, request, send_from_directory
import cv2
import numpy as np
from rice_count import count_rice_seeds
from maize_count import count_maize_seeds
from millet_count import count_millet_seeds

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', '.pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

# Ensure upload and processed folders exist
for folder in [UPLOAD_FOLDER, PROCESSED_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def index():
    seed_count = None
    seed_type = None
    image_filename = None
    processed_image_path = None

    if request.method == 'POST':
        seed_type = request.form['seed_type']
        if 'file' not in request.files:
            return render_template("index.html", error="No file uploaded!")

        file = request.files['file']
        if file.filename == '' or not allowed_file(file.filename):
            return render_template("index.html", error="Invalid file type!")

        image_filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
        file.save(file_path)

        # Process image based on seed type
        if seed_type == "rice":
            seed_count, processed_img = count_rice_seeds(file_path)
        elif seed_type == "maize":
            seed_count, processed_img = count_maize_seeds(file_path)
        elif seed_type == "millet":
            seed_count, processed_img = count_millet_seeds(file_path)
        else:
            return render_template("index.html", error="Invalid seed type!")

        # Save processed image
        processed_image_filename = f"processed_{image_filename}"
        processed_image_path = os.path.join(app.config['PROCESSED_FOLDER'], processed_image_filename)
        cv2.imwrite(processed_image_path, processed_img)

        return render_template("index.html", 
                               seed_count=seed_count, 
                               seed_type=seed_type, 
                               image_filename=image_filename, 
                               processed_image_filename=processed_image_filename)

    return render_template("index.html")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/processed_images/<filename>')
def processed_file(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True)
