from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .database import sql_db
models_sql_db = SQLAlchemy()
from app import db

app = Flask(__name__)
class Sala(sql_db.Model):
    id = sql_db.Column(sql_db.Integer, primary_key=True)
    nome = sql_db.Column(sql_db.String(100), nullable=False)
    disponivel = sql_db.Column(sql_db.Boolean, default=True)

    def __init__(self, nome):
        self.nome = nome

    def __repr__(self):
        return f"Sala('{self.nome}')"

class Reserva(sql_db.Model):
    id = sql_db.Column(sql_db.Integer, primary_key=True)
    sala_id = sql_db.Column(sql_db.Integer, sql_db.ForeignKey('sala.id'))
    usuario = sql_db.Column(sql_db.String(100), nullable=False)
    inicio = sql_db.Column(sql_db.DateTime, nullable=False)
    fim = sql_db.Column(sql_db.DateTime, nullable=False)

    def __init__(self, sala_id, usuario, inicio, fim):
        self.sala_id = sala_id
        self.usuario = usuario
        self.inicio = inicio
        self.fim = fim

    def __repr__(self):
        return f"Reserva('{self.usuario}', '{self.inicio}', '{self.fim}')"