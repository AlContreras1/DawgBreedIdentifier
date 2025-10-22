from flask import Flask, render_template, request, redirect, session, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'dog_secret_key'

# Folder to store uploaded dog images
UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# -------------------- ROUTES --------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/dashboard')
def dashboard():
    # This page will show results or uploaded images later
    return render_template('dashboard.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'dog_image' not in request.files:
        flash('No file uploaded!', 'danger')
        return redirect(url_for('index'))

    file = request.files['dog_image']

    if file.filename == '':
        flash('No selected file!', 'warning')
        return redirect(url_for('index'))

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        flash('Dog image uploaded successfully!', 'success')
        return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True)
W