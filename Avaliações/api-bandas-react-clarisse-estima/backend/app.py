from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import sqlite3
import hashlib
import logging
from flask_cors import CORS  # Para permitir requisições do React

app = Flask(__name__)
app.secret_key = 'sua_secret_key'
app.config['JWT_SECRET_KEY'] = 'seu_jwt_secret_key'
jwt = JWTManager(app)
CORS(app)  # Habilita CORS para aceitar requisições de outro domínio
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

@app.route('/register', methods=['POST'])
def register():
    email = request.json.get('email')
    password = request.json.get('password')
    
    logging.info(f"Cadastro com o email: {email}")

    if not email or not password:
        return jsonify(message="Email e senha são obrigatórios"), 400

    if user_exists(email):
        return jsonify(message="Usuário já existe"), 400

    hashed_password = hash_password(password)
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_password))
        conn.commit()

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
        access_token = create_access_token(identity=str(user[0]))
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
    cur.execute("SELECT * FROM integrantes")
    integrantes = cur.fetchall()
    conn.close()
    return jsonify(integrantes)

if __name__ == '__main__':
    app.run(debug=True)
