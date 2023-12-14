from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Configuración de la base de datos (SQLite)
DATABASE = 'usuarios.db'

def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    create_table()
    return render_template('index.html')

@app.route('/signin', methods=['POST'])
def signin():
    username = request.form['username']
    password = request.form['password']

    # Validar que al menos hay una mayúscula en la contraseña
    if not any(c.isupper() for c in password):
        return jsonify({'success': False, 'message': 'La contraseña debe contener al menos una mayúscula'})

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Consultar si el usuario y la contraseña coinciden en la base de datos
    cursor.execute("SELECT * FROM usuarios WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()

    conn.close()

    if user:
        return jsonify({'success': True, 'message': 'Inicio de sesión exitoso'})
    else:
        return jsonify({'success': False, 'message': 'Credenciales incorrectas'})

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    # Validar que al menos hay una mayúscula en la contraseña
    if not any(c.isupper() for c in password):
        return jsonify({'success': False, 'message': 'La contraseña debe contener al menos una mayúscula'})

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Verificar si el usuario ya existe en la base de datos
    cursor.execute("SELECT * FROM usuarios WHERE username=?", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        return jsonify({'success': False, 'message': 'El usuario ya está registrado'})

    # Insertar el nuevo usuario en la base de datos
    cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Registro exitoso'})

if __name__ == '__main__':
    app.run(debug=True)
