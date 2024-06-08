from sqlalchemy import create_engine, Column, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

# Configurações do banco de dados
engine = create_engine('sqlite:///usuarios.db')
Base = declarative_base()

# Definição da tabela de usuários
class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(String, primary_key=True)
    nome = Column(String)
    email = Column(String)
    telefone = Column(String)
    eh_entregador = Column(Boolean)

# Criação do banco de dados
Base.metadata.create_all(engine)
