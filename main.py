from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Make sure this folder exists (create it if not)
UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024  # optional: 8 MB limit

# Temporary in-memory storage
dogs = []
# last uploaded image filename to show on dashboard
uploaded_image = None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    global uploaded_image
    return render_template('dashboard.html', uploaded_image=uploaded_image)


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/dogs')
def dog_list():
    return render_template('dogs.html', dogs=dogs)


@app.route('/add', methods=['GET', 'POST'])
def add_dog():
    if request.method == 'POST':
        name = request.form.get('name', '')
        breed = request.form.get('breed', '')
        age = request.form.get('age', '')
        image = request.files.get('image')

        filename = None
        if image and image.filename:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        dogs.append({
            'id': len(dogs),
            'name': name,
            'breed': breed,
            'age': age,
            'image': filename
        })
        return redirect(url_for('dog_list'))

    return render_template('add_dog.html')


# THIS is the required endpoint referenced by url_for('upload')
@app.route('/upload', methods=['POST'])
def upload():
    global uploaded_image

    dog_img = request.files.get('dog_image')
    if not dog_img or dog_img.filename == '':
        # no file uploaded; redirect home safely
        return redirect(url_for('index'))

    filename = secure_filename(dog_img.filename)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    dog_img.save(save_path)

    uploaded_image = filename
    return redirect(url_for('dashboard'))


@app.route('/delete/<int:id>')
def delete_dog(id):
    if 0 <= id < len(dogs):
        dogs.pop(id)
    return redirect(url_for('dog_list'))


if __name__ == "__main__":
    # Use debug=True only for local development
    app.run(debug=True)
