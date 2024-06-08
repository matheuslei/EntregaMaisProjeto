from sqlalchemy.orm import sessionmaker
from models import engine, Usuario
import uuid

# Funções do banco de dados
def get_session():
    Session = sessionmaker(bind=engine)
    return Session()

def get_all_users():
    session = get_session()
    users = session.query(Usuario).all()
    session.close()
    return users

def insert_user(nome, email, telefone, eh_entregador):
    session = get_session()
    id = str(uuid.uuid4())
    user = Usuario(id=id, nome=nome, email=email, telefone=telefone, eh_entregador=eh_entregador)
    session.add(user)
    session.commit()
    session.close()

def update_user(id, nome, email, telefone, eh_entregador):
    session = get_session()
    user = session.query(Usuario).filter_by(id=id).first()
    user.nome = nome
    user.email = email
    user.telefone = telefone
    user.eh_entregador = eh_entregador
    session.commit()
    session.close()

def get_user(id):
    session = get_session()
    user = session.query(Usuario).filter_by(id=id).first()
    session.close()
    return user

def delete_user(id):
    session = get_session()
    user = session.query(Usuario).filter_by(id=id).first()
    session.delete(user)
    session.commit()
    session.close()
