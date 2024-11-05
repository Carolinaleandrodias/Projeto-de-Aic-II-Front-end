from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, current_user, UserMixin
from werkzeug.security import check_password_hash
from .models import Usuario
from .forms import LoginForm
from . import db 

# Blueprint de usuários
usuarios = Blueprint('usuarios', __name__)

# Modelo de Usuário
class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha = db.Column(db.String(150), nullable=False)
    nome = db.Column(db.String(150), nullable=False)
    tipo = db.Column(db.String(50), default='usuario')  # 'usuario' ou 'admin'

# Rota de Login
@usuarios.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and check_password_hash(usuario.senha, form.senha.data):
            login_user(usuario)
            flash('Login realizado com sucesso!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('main.index'))
        else:
            flash('Email ou senha inválidos.', 'danger')
    return render_template('login.html', form=form)

# Rota de Perfil do Usuário
@usuarios.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html', usuario=current_user)
