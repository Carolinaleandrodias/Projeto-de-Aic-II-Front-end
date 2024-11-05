from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from .models import db, Reserva, Usuario, Sala
from .forms import ReservaForm, LoginForm
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
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

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('main.index'))

@main.route('/reservar', methods=['GET', 'POST'])
@login_required
def reservar():
    form = ReservaForm()
    # Preencher as escolhas de sala no formulário
    form.sala_id.choices = [(s.id, f'Sala {s.numero} - Capacidade: {s.capacidade}') 
                           for s in Sala.query.all()]
    
    if form.validate_on_submit():
        # Verificar se a sala está disponível
        sala_ocupada = Reserva.query.filter(
            Reserva.sala_id == form.sala_id.data,
            Reserva.inicio <= form.fim.data,
            Reserva.fim >= form.inicio.data
        ).first()
        
        if sala_ocupada:
            flash('Esta sala já está reservada para este horário.', 'danger')
        else:
            reserva = Reserva(
                sala_id=form.sala_id.data,
                usuario=current_user.nome,
                inicio=form.inicio.data,
                fim=form.fim.data
            )
            db.session.add(reserva)
            db.session.commit()
            flash('Reserva realizada com sucesso!', 'success')
            return redirect(url_for('main.consultar'))
            
    return render_template('reservar.html', form=form)

@main.route('/consultar')
@login_required
def consultar():
    reservas = Reserva.query.all()
    return render_template('consultar.html', reservas=reservas)

@main.route('/minhas_reservas')
@login_required
def minhas_reservas():
    reservas = Reserva.query.filter_by(usuario=current_user.nome).all()
    return render_template('minhas_reservas.html', reservas=reservas)

@main.route('/cancelar_reserva/<int:id>')
@login_required
def cancelar_reserva(id):
    reserva = Reserva.query.get_or_404(id)
    if reserva.usuario == current_user.nome:
        db.session.delete(reserva)
        db.session.commit()
        flash('Reserva cancelada com sucesso!', 'success')
    else:
        flash('Você não tem permissão para cancelar esta reserva.', 'danger')
    return redirect(url_for('main.minhas_reservas'))
