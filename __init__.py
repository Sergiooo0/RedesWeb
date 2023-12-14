from flask import Flask, render_template, request, url_for, redirect, session

app = Flask("Hola")
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'super secret key'

@app.route('/')
def hello():
  title="Mi primera página web"
  return render_template('index.html',title=title, usuario=(session['usuario'] if 'usuario' in session else None))

@app.route('/login', methods=['POST', 'GET'])
def login():
   username = request.form.get('username')
   password = request.form.get('password')
   print("Username: "+str(username)+" Password: "+str(password))
   if username == "root" and password == "toor":
     session['usuario']=username
    
   return redirect(url_for('hello'))

@app.route('/logout')
def logout():
   session.clear()
   return redirect(url_for('hello'))
