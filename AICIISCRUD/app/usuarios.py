from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, current_user, UserMixin, logout_user
from werkzeug.security import check_password_hash
from .models import Usuario, Booking, Affiliation
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

@usuarios.route('/book_tile', methods=['POST'])
@login_required
def book_tile():
    data = request.get_json()
    slot = data['slot']
    day = data['day']
    room = data['room']
    email = data['email']
    week_start = datetime.strptime(data['weekStart'], '%Y-%m-%d').date()
    # Check if the user has already booked this slot in another room
    existing_booking = Booking.query.filter_by(slot=slot, day=day, email=email, week_start=week_start).first()
    if existing_booking:
        return jsonify(success=False, message="You have already booked this slot in another room.")
    # Save booking info to the database
    booking = Booking(slot=slot, day=day, room=room, email=email, week_start=week_start)
    db.session.add(booking)
    db.session.commit()
    return jsonify(success=True)

@usuarios.route('/unbook_tile', methods=['POST'])
@login_required
def unbook_tile():
    data = request.get_json()
    slot = data['slot']
    day = data['day']
    room = data['room']
    week_start = datetime.strptime(data['weekStart'], '%Y-%m-%d').date()
    # Remove booking info from the database
    Booking.query.filter_by(slot=slot, day=day, room=room, week_start=week_start).delete()
    db.session.commit()
    return jsonify(success=True)

@usuarios.route('/get_bookings')
@login_required
def get_bookings():
    week_start = request.args.get('start')
    week_start_date = datetime.strptime(week_start, '%Y-%m-%d').date()
    bookings = Booking.query.filter_by(week_start=week_start_date).all()
    return jsonify(bookings=[{
        'id': booking.id,
        'slot': booking.slot,
        'day': booking.day,
        'room': booking.room,
        'email': booking.email,
        'week_start': booking.week_start.isoformat()
    } for booking in bookings])

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
            # Redirect to the perfil page
            return redirect(url_for('usuarios.perfil', usuario=current_user))
        else:
            # If email or password is incorrect, show a flash message
            print("Email or password is incorrect")
            flash('Email ou senha inválidos.', 'danger')
            # Redirect back to the login page so the user can try again
            return render_template('index.html')  # redirect to the login route

    return render_template('index.html')



@usuarios.route('/registrar', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        confirm_senha = request.form.get('confirm_senha')
        matricula = request.form.get('matricula')
        user_type = request.form.get('user_type')
        favorite_color = request.form.get('favorite_color') if user_type == '2' else 'orange'

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
            senha=senha,
            matricula=matricula,
            user_type=int(user_type),
            favorite_color=favorite_color
        )

        db.session.add(usuario)
        db.session.commit()
        flash('Conta criada com sucesso', 'success')
        return render_template('index.html')

    return render_template('index.html')



@usuarios.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    if request.method == 'POST':
        nome = request.form.get('nome')
        favorite_color = request.form.get('favorite_color') if current_user.user_type == 1 else current_user.favorite_color
        senha_atual = request.form.get('senha_atual')
        nova_senha = request.form.get('nova_senha')
        confirm_nova_senha = request.form.get('confirm_nova_senha')

        if nova_senha and nova_senha != confirm_nova_senha:
            flash('As novas senhas não coincidem', 'danger')
            return redirect(url_for('usuarios.perfil'))

        if nova_senha and senha_atual != current_user.senha:
            flash('A senha atual está incorreta', 'danger')
            return redirect(url_for('usuarios.perfil'))

        current_user.nome = nome
        current_user.favorite_color = favorite_color

        if nova_senha:
            current_user.senha = nova_senha

        db.session.commit()
        flash('Perfil atualizado com sucesso', 'success')
        return redirect(url_for('usuarios.perfil'))
    
    professors = Usuario.query.filter_by(user_type=1).all()
    affiliations = [aff.professor_id for aff in Affiliation.query.filter_by(student_id=current_user.id).all()]
    return render_template('perfil.html', usuario=current_user, professors=professors, affiliations=affiliations)

@usuarios.route('/update_affiliation', methods=['POST'])
@login_required
def update_affiliation():
    if current_user.user_type != 2:
        return jsonify({'error': 'Unauthorized'}), 403

    professor_id = request.form.get('professor_id')
    action = request.form.get('action')

    if action == 'add':
        new_affiliation = Affiliation(student_id=current_user.id, professor_id=int(professor_id))
        db.session.add(new_affiliation)
    elif action == 'remove':
        Affiliation.query.filter_by(student_id=current_user.id, professor_id=int(professor_id)).delete()

    db.session.commit()
    return jsonify({'success': True})

@usuarios.route('/agenda')
@login_required
def agenda():
    # Get professor emails for student affiliation
    affiliations = [aff.professor_id for aff in Affiliation.query.filter_by(student_id=current_user.id).all()]
    professor_emails = [prof.email for prof in Usuario.query.filter(Usuario.id.in_(affiliations)).all()]
    
    # Get all professor names
    professors = Usuario.query.filter_by(user_type=1).all()
    professor_names = {prof.email: prof.nome for prof in professors}
    
    return render_template('agenda.html', 
                         professor_emails=professor_emails,
                         professor_names=professor_names)



@usuarios.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado com sucesso.', 'success')
    return redirect(url_for('usuarios.login'))