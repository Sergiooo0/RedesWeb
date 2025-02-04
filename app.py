from flask import Flask, render_template, redirect, url_for, request, jsonify, session
import mysql.connector

app = Flask("Mi web")
app.secret_key = 'super secret key'
# Configuración de la base de datos (MySQL)
DATABASE = {
    'host': 'mysql-sergiogonzalez.alwaysdata.net',
    'user': '340093_yo',
    'password': '**********',
    'database': 'sergiogonzalez_yo'
}


def create_table():
    with mysql.connector.connect(**DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL
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

    # Establecer la conexión a MySQL
    conn = mysql.connector.connect(**DATABASE)
    cursor = conn.cursor()

    # Consultar si el usuario y la contraseña coinciden en la base de datos
    cursor.execute("SELECT * FROM usuarios WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()

    # Cerrar la conexión
    cursor.close()
    conn.close()

    if user:
        session['usuario'] = username
        return redirect(url_for('dashboard'))
    else:
        return "Credenciales incorrectas"
    
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    # Establecer la conexión a MySQL
    conn = mysql.connector.connect(**DATABASE)
    cursor = conn.cursor()

    # Verificar si el usuario ya existe en la base de datos
    cursor.execute("SELECT * FROM usuarios WHERE username=%s", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        # Cerrar la conexión
        cursor.close()
        conn.close()
        return "El usuario ya está registrado"

    # Insertar el nuevo usuario en la base de datos
    cursor.execute("INSERT INTO usuarios (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()

    # Cerrar la conexión
    cursor.close()
    conn.close()

    session['usuario'] = username
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
