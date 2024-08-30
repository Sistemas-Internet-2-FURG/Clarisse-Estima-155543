# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Database opened successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS bandas (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT)')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS integrantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            nome TEXT, 
            banda_id INTEGER, 
            FOREIGN KEY (banda_id) REFERENCES bandas (id)
        )
    ''')
    print("Tabelas criadas")
    conn.close()

init_sqlite_db()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/bandas')
def listar_bandas():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM bandas")
    bandas = cur.fetchall()
    conn.close()
    return render_template('listar_bandas.html', bandas=bandas)

@app.route('/bandas/add', methods=['POST'])
def adicionar_bandas():
    if request.method == 'POST':
        try:
            nome = request.form['nome']
            conn = sqlite3.connect('database.db')
            cur = conn.cursor()
            cur.execute("INSERT INTO bandas (nome) VALUES (?)", (nome,))
            conn.commit()
            conn.close()
            return redirect(url_for('listar_bandas'))
        except Exception as e:
            return str(e)

@app.route('/integrantes')
def listar_integrantes():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT integrantes.id, integrantes.nome, bandas.nome FROM integrantes JOIN bandas ON integrantes.banda_id = bandas.id")
    integrantes = cur.fetchall()
    conn.close()
    return render_template('listar_integrantes.html', integrantes=integrantes)

@app.route('/integrantes/add', methods=['GET', 'POST'])
def adicionar_integrantes():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    if request.method == 'POST':
        try:
            nome = request.form['nome']
            banda_id = request.form['banda_id']
            cur.execute("INSERT INTO integrantes (nome, banda_id) VALUES (?, ?)", (nome, banda_id))
            conn.commit()
            return redirect(url_for('listar_integrantes'))
        except Exception as e:
            return str(e)
    else:
        cur.execute("SELECT * FROM bandas")
        bandas = cur.fetchall()
        conn.close()
        return render_template('listar_integrantes.html', bandas=bandas)



@app.route('/bandas/edit/<int:id>', methods=['GET', 'POST'])
def editar_bandas(id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    if request.method == 'POST':
        nome = request.form['nome']
        cur.execute("UPDATE bandas SET nome = ? WHERE id = ?", (nome, id))
        conn.commit()
        conn.close()
        return redirect(url_for('listar_bandas'))

    cur.execute("SELECT * FROM bandas WHERE id = ?", (id,))
    banda = cur.fetchone()
    conn.close()
    return render_template('editar_bandas.html', banda=banda)

@app.route('/integrantes/edit/<int:id>', methods=['GET', 'POST'])
def editar_integrantes(id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    if request.method == 'POST':
        nome = request.form['nome']
        banda_id = request.form['banda_id']
        cur.execute("UPDATE integrantes SET nome = ?, banda_id = ? WHERE id = ?", (nome, banda_id, id))
        conn.commit()
        conn.close()
        return redirect(url_for('listar_integrantes'))

    cur.execute("SELECT * FROM integrantes WHERE id = ?", (id,))
    integrante = cur.fetchone()
    cur.execute("SELECT * FROM bandas")
    bandas = cur.fetchall()
    conn.close()
    return render_template('editar_integrantes.html', integrante=integrante, bandas=bandas)

@app.route('/bandas/delete/<int:id>', methods=['GET'])
def deletar_banda(id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM bandas WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('listar_bandas'))

@app.route('/integrantes/delete/<int:id>', methods=['GET'])
def deletar_integrante(id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM integrantes WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('listar_integrantes'))

if __name__ == '__main__':
    app.run(debug=True)

