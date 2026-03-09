from sqlalchemy import Column, Integer, String, ForeignKey
from flask_login import UserMixin
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Administrador(Base, UserMixin):
    __tablename__ = "administradores"
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=True)
    cargo = Column(String(100), nullable=True)
    email = Column(String(100), unique=True, nullable=True)
    senha = Column(String(50), nullable=True)


class Voluntario(Base):
    __tablename__ = "voluntarios"
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=True)
    disponibilidade =  Column(String(300), nullable=True)
    tipo_apoio =  Column(String(300), nullable=True)
    email = Column(String(50), unique=True, nullable=True)

class Solicitante(Base):
    __tablename__ = "solicitantes"
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=True)
    dificuldade = Column(String(300), nullable=True)  
    horario_disponivel = Column(String(50), nullable=True)
    email = Column(String(100), unique=True, nullable=True)

class Atendimento(Base):
    __tablename__ = "atendimentos"
    id = Column(Integer, primary_key=True)
    voluntario_id = Column(Integer, ForeignKey("voluntarios.id"))
    solicitante_id = Column(Integer, ForeignKey("solicitantes.id"))
    voluntario = relationship("Voluntario")
    solicitante = relationship("Solicitante")