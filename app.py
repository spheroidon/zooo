from flask import Flask, render_template, request, redirect, send_from_directory, url_for
import sqlite3
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'  # Set your desired upload folder

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Function to create the database table if it doesn't exist
def create_table():
    conn = sqlite3.connect('animals.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS animals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            species TEXT NOT NULL,
            age INT NOT NULL,
            photo TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_table()

# Route to display all animals
@app.route('/')
def index():
    conn = sqlite3.connect('animals.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM animals')
    animals = cursor.fetchall()
    conn.close()
    return render_template('index.html', animals=animals)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/add', methods=['POST'])
def add_animal():
    name = request.form['name']
    species = request.form['species']
    age = request.form['age']
    photo = request.files['photo']

    if photo:
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    else:
        photo_path = None

    conn = sqlite3.connect('animals.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO animals (name, species, age, photo) VALUES (?, ?, ?, ?)', (name, species, age, photo_path))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

# Route to delete a animal
@app.route('/delete/<int:animal_id>')
def delete_animal(animal_id):
    conn = sqlite3.connect('animals.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM animals WHERE id = ?', (animal_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

# Route to edit a animal (displaying the form for editing)
@app.route('/edit/<int:animal_id>')
def edit_animal(animal_id):
    conn = sqlite3.connect('animals.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM animals WHERE id = ?', (animal_id,))
    animal = cursor.fetchone()
    conn.close()
    return render_template('edit.html', animal=animal)

@app.route('/update/<int:animal_id>', methods=['POST'])
def update_animal(animal_id):
    name = request.form['name']
    species = request.form['species']
    age = request.form['age']
    new_photo = request.files['photo']

    conn = sqlite3.connect('animals.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM animals WHERE id = ?', (animal_id,))
    animal = cursor.fetchone()

    if new_photo:
        # If a new photo is uploaded, handle it similar to adding a new animal's photo
        filename = secure_filename(new_photo.filename)
        new_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    else:
        # If no new photo uploaded, keep the old photo path
        photo_path = animal[4]

    cursor.execute('UPDATE animals SET name = ?, species = ?, age = ?, photo = ? WHERE id = ?', (name, species, age, photo_path, animal_id))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
