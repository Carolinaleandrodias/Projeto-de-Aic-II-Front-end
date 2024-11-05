from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Email, ValidationError
from datetime import datetime

class ReservaForm(FlaskForm):
    sala_id = SelectField('Sala', coerce=int, validators=[DataRequired()])
    inicio = DateTimeField('Início', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    fim = DateTimeField('Fim', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    submit = SubmitField('Reservar')

    def validate_fim(self, field):
        if field.data <= self.inicio.data:
            raise ValidationError('O horário de fim deve ser posterior ao horário de início.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class SalaForm(FlaskForm):
    numero = StringField('Número da Sala', validators=[DataRequired()])
    capacidade = IntegerField('Capacidade', validators=[DataRequired()])
    submit = SubmitField('Adicionar Sala')