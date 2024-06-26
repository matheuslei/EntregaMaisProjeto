from flask import Flask, render_template, request, redirect, url_for, session, flash
from db_functions import get_all_users, insert_user, update_user, get_user, delete_user

app = Flask(__name__)
app.secret_key = 'admin'

def check_authentication():
    if 'username' not in session or 'password' not in session:
        return False
    return session['username'] == "admin" and session['password'] == "admin"

@app.route('/consulta', methods=['GET'])
def consulta():
    if not check_authentication():
        return redirect(url_for('login'))

    data = get_all_users()
    editing_id = request.args.get('edit')
    deleted_id = request.args.get('deleted_id')
    
    if deleted_id:
        delete_user(deleted_id)
        data = [user for user in data if user.id != deleted_id]  # Remove usuário excluído da lista
    
    return render_template('consulta.html', data=data, editing_id=editing_id)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        eh_entregador = bool(request.form.get('eh_entregador'))
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
        eh_entregador = bool(request.form.get('eh_entregador'))
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
        if username == "admin" and password == "admin":
            session['username'] = username
            session['password'] = password
            return redirect(url_for('consulta'))
        else:
            flash('Usuário ou senha inválidos', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('password', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
