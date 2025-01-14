from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, current_user, UserMixin
from werkzeug.security import check_password_hash
from .models import Usuario
from .forms import LoginForm, RegisterForm
from flask import jsonify
from . import db 

# Blueprint de usuários
usuarios = Blueprint('usuarios', __name__)

# Modelo de Usuário
# Usuario se refere ao blueprint e à rota de usuários, lidar com o processo de login, perfil e autenticação do usuário
# Gerencia as interações com a interface da aplicação e controlar o acesso das rotas.

# Rota de Login

@usuarios.route('/header-test')
def header_test():
    return render_template('header.html')   
  

@usuarios.route('/perfil', methods=['GET', 'POST'])
def login():
    # If the user is already authenticated, redirect them to the main page
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()

    if form.validate_on_submit():
        # Check for the user by email
        usuario = Usuario.query.filter_by(email=form.email.data).first()

        # If the user exists and the password matches
        if usuario and usuario.senha == form.senha.data:
            login_user(usuario)  # Log the user in
            flash('Login realizado com sucesso!', 'success')

            next_page = request.args.get('next')
            # Redirect to the next page if available, otherwise to the main page
            return redirect(next_page if next_page else url_for('main.index'))
        else:
            # If email or password is incorrect, show a flash message
            flash('Email ou senha inválidos.', 'danger')
            # Redirect back to the login page so the user can try again
            return redirect(url_for('usuarios.login'))  # redirect to the login route

    return render_template('login.html', form=form)



@usuarios.route('/registrar', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        matricula = request.form.get('matricula')

        # Verificar se já existe um usuário com o mesmo email ou matrícula
        usuario_existente = Usuario.query.filter(
            (Usuario.email == email) | (Usuario.matricula == matricula)
        ).first()
        if usuario_existente:
            flash('Já existe um usuário com este e-mail ou matrícula.', 'danger')
            return redirect(url_for('usuarios.register'))

        # Criar novo usuário
        usuario = Usuario(
            nome=nome,
            email=email,
            senha=senha,  # Lembre-se de usar hash na senha em produção!
            matricula=int(matricula)
        )

        try:
            db.session.add(usuario)
            db.session.commit()
            flash('Cadastro realizado com sucesso! Faça login agora.', 'success')
            return redirect(url_for('usuarios.agenda'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar usuário: {e}', 'danger')  # Log detalhado do erro
            return redirect(url_for('usuarios.register'))

    # Redireciona diretamente para a página de login no método GET
    return render_template('agenda.html')



    
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
