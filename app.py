from flask import Flask, render_template, redirect, url_for, request, jsonify, session
import sqlite3

app = Flask("Mi web")
app.secret_key = 'super secret key'
# Configuración de la base de datos (SQLite)
DATABASE = 'usuarios.db'

def create_table():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')

@app.route('/')
def index():
    create_table()
    return render_template('index.html', usuario=(session['usuario'] if 'usuario' in session else None))

@app.route('/signin')
def signin():
    return render_template('index.html', usuario=(session['usuario'] if 'usuario' in session else None))

@app.route('/registro')
def registro():
    return render_template('index.html', usuario=(session['usuario'] if 'usuario' in session else None))

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        # Consultar si el usuario y la contraseña coinciden en la base de datos
        cursor.execute("SELECT * FROM usuarios WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()

    if user:
        session['usuario']=username
        return redirect(url_for('dashboard'))
    else:
        return "Credenciales incorrectas"

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        # Verificar si el usuario ya existe en la base de datos
        cursor.execute("SELECT * FROM usuarios WHERE username=?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            return "El usuario ya está registrado"
        
        # Insertar el nuevo usuario en la base de datos
        cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, password))
        conn.commit()

    session['usuario']=username
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
   session.clear()
   return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
