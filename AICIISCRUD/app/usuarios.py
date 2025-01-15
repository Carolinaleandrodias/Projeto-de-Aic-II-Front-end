from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, current_user, UserMixin, logout_user
from werkzeug.security import check_password_hash
from .models import Usuario
from .forms import LoginForm, RegisterForm
from flask import jsonify
from datetime import datetime
from . import db
# Blueprint de usuários
usuarios = Blueprint('usuarios', __name__)
main = Blueprint('main', __name__)

# As rotas de login e de registrar conta estão no usuarios.py

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('main.index'))

# Modelo de Usuário
# Usuario se refere ao blueprint e à rota de usuários, lidar com o processo de login, perfil e autenticação do usuário
# Gerencia as interações com a interface da aplicação e controlar o acesso das rotas.

# Rota de Login

@usuarios.route('/header-test')
def header_test():
    return render_template('header.html')   
  

@usuarios.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        # Check for the user by email
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario:
            print(f"User found: {usuario.email}")
        else:
            print("User not found")
        
        # If the user exists and the password matches
        if usuario and usuario.senha == senha:
            print("Password matches")
            login_user(usuario)  # Log the user in
            flash('Login realizado com sucesso!', 'success')
            # Redirect to the next page if available, otherwise to the main page
            return render_template('perfil.html', usuario=current_user)
        else:
            # If email or password is incorrect, show a flash message
            print("Email or password is incorrect")
            flash('Email ou senha inválidos.', 'danger')
            # Redirect back to the login page so the user can try again
            return render_template('index.html')  # redirect to the login route

    return render_template('perfil.html', usuario=current_user)



@usuarios.route('/registrar', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        confirm_senha = request.form.get('confirm_senha')
        matricula = request.form.get('matricula')

        # Check if the passwords match
        if senha != confirm_senha:
            flash('As senhas não coincidem.', 'danger')
            return render_template('index.html')

        # Check if the user already exists
        usuario_existente = Usuario.query.filter((Usuario.email == email) | (Usuario.matricula == matricula)).first()
        if usuario_existente:
            flash('Já existe um usuário com este e-mail ou matrícula.', 'danger')
            return render_template('index.html')

        # Create a new user without hashing the password
        usuario = Usuario(
            nome=nome,
            email=email,
            senha=senha,  # Store the password as plain text
            matricula=int(matricula)
        )

        try:
            db.session.add(usuario)
            db.session.commit()
            flash('Cadastro realizado com sucesso! Faça login agora.', 'success')
            return render_template('index.html')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar usuário: {e}', 'danger')  # Log detailed error
            return render_template('index.html')

    return render_template('index.html')



    
@usuarios.route('/special', methods=['GET'])
def special():
    try:
        usuarios = Usuario.query.all()
        print(usuarios, len(usuarios))
        usuarios_list = [{'id': usuario.id, 'nome': usuario.nome, 'email': usuario.email, 'tipo': usuario.tipo} for usuario in usuarios]

        return jsonify(usuarios_list)
    except Exception as error:
        print("DEU ERRO NESSA PORRA", error)
        return "Deu ruimzao"

# Rota de Perfil do Usuário
@usuarios.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html', usuario=current_user)
