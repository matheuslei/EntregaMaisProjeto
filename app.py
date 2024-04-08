from flask import Flask, render_template, request, redirect, url_for, session, flash
import pyodbc
import uuid

app = Flask(__name__)
app.secret_key = 'admin'

# Configurações do banco de dados
server = 'SEN13119\\SQLEXPRESS'
database = 'EntregaMais'
driver = '{ODBC Driver 17 for SQL Server}'

# Variáveis de autenticação
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin'

def connect_database():
    return pyodbc.connect(
        'DRIVER=' + driver +
        ';SERVER=' + server +
        ';DATABASE=' + database +
        ';Trusted_Connection=yes;'
    )

# Funções do banco de dados
def get_all_users():
    with connect_database() as conn:
        cursor = conn.cursor()
        select_query = "SELECT * FROM usuarios"
        cursor.execute(select_query)
        data = cursor.fetchall()
    return data

def insert_user(nome, email, telefone, eh_entregador):
    with connect_database() as conn:
        cursor = conn.cursor()
        id = str(uuid.uuid4())
        insert_query = "INSERT INTO usuarios (id, nome, email, telefone, eh_entregador) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(insert_query, (id, nome, email, telefone, eh_entregador))
        conn.commit()

def update_user(id, nome, email, telefone, eh_entregador):
    with connect_database() as conn:
        cursor = conn.cursor()
        update_query = "UPDATE usuarios SET nome=?, email=?, telefone=?, eh_entregador=? WHERE id=?"
        cursor.execute(update_query, (nome, email, telefone, eh_entregador, id))
        conn.commit()

def get_user(id):
    with connect_database() as conn:
        cursor = conn.cursor()
        select_query = "SELECT * FROM usuarios WHERE id=?"
        cursor.execute(select_query, (id,))
        user = cursor.fetchone()
    return user

def delete_user(id):
    with connect_database() as conn:
        cursor = conn.cursor()
        delete_query = "DELETE FROM usuarios WHERE id=?"
        cursor.execute(delete_query, (id,))
        conn.commit()

def check_authentication():
    if 'username' not in session or 'password' not in session:
        return False
    return session['username'] == ADMIN_USERNAME and session['password'] == ADMIN_PASSWORD

@app.route('/consulta', methods=['GET'])
def consulta():
    if not check_authentication():
        return redirect(url_for('login'))

    data = get_all_users()
    editing_id = request.args.get('edit')
    deleted_id = request.args.get('deleted_id')
    
    if deleted_id:
        data = [user for user in data if user[0] != deleted_id]  # Remove usuário excluído da lista
    
    return render_template('consulta.html', data=data, editing_id=editing_id)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        eh_entregador = request.form.get('eh_entregador', False)
        if eh_entregador == 'on':
            eh_entregador = True
        else:
            eh_entregador = False
        insert_user(nome, email, telefone, eh_entregador)
    data = get_all_users()
    return render_template('index.html', data=data)


@app.route('/editar/<id>', methods=['GET', 'POST'])
def editar(id):
    if not check_authentication():
        return redirect(url_for('login'))

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        eh_entregador = 'eh_entregador' in request.form
        update_user(id, nome, email, telefone, eh_entregador)
        return redirect(url_for('consulta'))
    
    user = get_user(id)
    return render_template('editar.html', user=user)


@app.route('/consulta/excluir/<id>', methods=['POST'])
def excluir(id):
    if not check_authentication():
        return redirect(url_for('login'))

    delete_user(id)
    return redirect(url_for('consulta'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['username'] = username
            session['password'] = password
            return redirect(url_for('consulta'))
        else:
            flash('Usuário ou senha inválidos', 'error')
    return render_template('login.html')

# Adicione esta rota para logout em app.py
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('password', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
