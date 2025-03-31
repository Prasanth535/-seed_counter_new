import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import cv2
import numpy as np
from rice_count import count_rice_seeds
from maize_count import count_maize_seeds
from millet_count import count_millet_seeds

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def index():
    seed_count = None
    seed_type = None
    image_filename = None

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

        if seed_type == "rice":
            seed_count = count_rice_seeds(file_path)
        elif seed_type == "maize":
            seed_count = count_maize_seeds(file_path)
        elif seed_type == "millet":
            seed_count = count_millet_seeds(file_path)

        return render_template("index.html", seed_count=seed_count, seed_type=seed_type, image_filename=image_filename)

    return render_template("index.html")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True)
