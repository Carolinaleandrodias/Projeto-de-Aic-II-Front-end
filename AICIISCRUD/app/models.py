from flask import Flask
from flask_sqlalchemy import SQLAlchemy

models_sql_db = SQLAlchemy()

class Sala(models_sql_db.Model):
    id = models_sql_db.Column(models_sql_db.Integer, primary_key=True)
    nome = models_sql_db.Column(models_sql_db.String(100), nullable=False)
    disponivel = models_sql_db.Column(models_sql_db.Boolean, default=True)

    def __init__(self, nome):
        self.nome = nome

    def __repr__(self):
        return f"Sala('{self.nome}')"

class Reserva(models_sql_db.Model):
    id = models_sql_db.Column(models_sql_db.Integer, primary_key=True)
    sala_id = models_sql_db.Column(models_sql_db.Integer, models_sql_db.ForeignKey('sala.id'))
    usuario = models_sql_db.Column(models_sql_db.String(100), nullable=False)
    inicio = models_sql_db.Column(models_sql_db.DateTime, nullable=False)
    fim = models_sql_db.Column(models_sql_db.DateTime, nullable=False)

    def __init__(self, sala_id, usuario, inicio, fim):
        self.sala_id = sala_id
        self.usuario = usuario
        self.inicio = inicio
        self.fim = fim

    def __repr__(self):
        return f"Reserva('{self.usuario}', '{self.inicio}', '{self.fim}')"