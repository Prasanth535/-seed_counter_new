import os
from flask import Flask, render_template, request
import cv2
import numpy as np
from rice_count import count_rice_seeds
from maize_count import count_maize_seeds
from millet_count import count_millet_seeds

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
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
    image_path = None

    if request.method == 'POST':
        seed_type = request.form['seed_type']
        file = request.files.get('file')

        if not file or file.filename == '' or not allowed_file(file.filename):
            return render_template("index.html", error="Invalid or missing file!")

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        image_path = file_path  # Store image path for display

        # Process image based on selected seed type
        if seed_type == "rice":
            seed_count = count_rice_seeds(file_path)
        elif seed_type == "maize":
            seed_count = count_maize_seeds(file_path)
        elif seed_type == "millet":
            seed_count = count_millet_seeds(file_path)

        return render_template("index.html", seed_count=seed_count, seed_type=seed_type, image_path=image_path)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
