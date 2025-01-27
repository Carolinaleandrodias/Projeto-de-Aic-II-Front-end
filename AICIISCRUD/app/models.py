from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

db = SQLAlchemy()

class Usuario(db.Model, UserMixin):  # Inherit from UserMixin
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(128), nullable=False) 
    matricula = db.Column(db.Integer(), nullable=False)
    favorite_color = db.Column(db.String(50), default='orange')
    user_type = db.Column(db.Integer, nullable=False)  # 1 for Professor, 2 for Estudante
    affiliations = db.relationship('Affiliation', backref='student', lazy=True, foreign_keys='Affiliation.student_id')
    professor_affiliations = db.relationship('Affiliation', backref='professor', lazy=True, foreign_keys='Affiliation.professor_id')

class Affiliation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)


class Booking(db.Model): # É a classe que representa a reserva 
    id = db.Column(db.Integer, primary_key=True)
    slot = db.Column(db.Integer, nullable=False)
    day = db.Column(db.String(50), nullable=False)
    room = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    week_start = db.Column(db.Date, nullable=False)
