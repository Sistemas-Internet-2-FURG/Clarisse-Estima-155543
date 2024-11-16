from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import sqlite3
import hashlib
import logging

app = Flask(__name__)
app.secret_key = 'sua_secret_key'
app.config['JWT_SECRET_KEY'] = 'seu_jwt_secret_key' 
jwt = JWTManager(app)
logging.basicConfig(level=logging.INFO)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(email, password):
    hashed_password = hash_password(password)
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, hashed_password))
        return cur.fetchone()

def user_exists(email):
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM users WHERE email = ?", (email,))
        return cur.fetchone() is not None

@app.route('/')
def index():
    return render_template('login.html')  

@app.route('/register')
def register_page():
    return render_template('register.html') 

@app.route('/register', methods=['POST'])
def register():
    email = request.json.get('email')
    password = request.json.get('password')
    
    logging.info(f"Cadastro com o email: {email}")

    if not email or not password:
        return jsonify(message="Email e senha são obrigatórios"), 400

    if user_exists(email):
        return jsonify(message="Email já registrado"), 400

    hashed_password = hash_password(password)
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_password))
    conn.commit()
    conn.close()

    return jsonify(message="Usuário registrado com sucesso"), 201

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    logging.info(f"Tentativa de login para o email: {email}")

    if not email or not password:
        return jsonify(message="Email e senha são obrigatórios"), 400

    user = authenticate_user(email, password)

    if user:
        access_token = create_access_token(identity=user[0])
        logging.info(f"Access token: {access_token} do email: {email}")
        return jsonify(access_token=access_token), 200
    else:
        return jsonify(message="Credenciais inválidas"), 401

@app.route('/bandas', methods=['GET'])
@jwt_required()
def listar_bandas():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM bandas")
    bandas = cur.fetchall()
    conn.close()
    return jsonify(bandas)


@app.route('/integrantes', methods=['GET'])
@jwt_required()
def listar_integrantes():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT integrantes.id, integrantes.nome, bandas.nome FROM integrantes JOIN bandas ON integrantes.banda_id = bandas.id")
    integrantes = cur.fetchall()
    conn.close()
 
    return jsonify(integrantes)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Database criada")
    conn.execute('CREATE TABLE IF NOT EXISTS bandas (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS integrantes (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, banda_id INTEGER)')
    conn.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT NOT NULL UNIQUE, password TEXT NOT NULL)''')
    conn.close()

if __name__ == '__main__':
    init_sqlite_db()
    app.run(debug=True)
