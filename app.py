from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

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

# Route to add a new animal
@app.route('/add', methods=['POST'])
def add_animal():
    name = request.form['name']
    species = request.form['species']
    age = request.form['age']
    photo = request.form['photo']

    conn = sqlite3.connect('animals.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO animals (name, species, age, photo) VALUES (?, ?, ?, ?)', (name, species, age, photo))
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

# Route to update a animal after editing
@app.route('/update/<int:animal_id>', methods=['POST'])
def update_animal(animal_id):
    name = request.form['name']
    species = request.form['species']
    age = request.form['age']
    photo = request.form['photo']

    conn = sqlite3.connect('animals.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE animals SET name = ?, species = ?, age = ?, photo = ? WHERE id = ?', (name, species, age, photo, animal_id))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
