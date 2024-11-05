from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .models import Sala
from .forms import SalaForm
from .reservas import db

salas = Blueprint('salas', __name__)

@salas.route('/')
@login_required
def listar_salas():
    salas = Sala.query.all()  # Obtém todas as salas do banco de dados
    return render_template('listar_salas.html', salas=salas)

@salas.route('/adicionar', methods=['GET', 'POST'])
@login_required
def adicionar_sala():
    if not current_user.tipo == 'admin':
        flash('Acesso negado. Apenas administradores podem adicionar salas.', 'danger')
        return redirect(url_for('salas.listar_salas'))
    
    form = SalaForm()
    if form.validate_on_submit():
        sala_existente = Sala.query.filter_by(numero=form.numero.data).first()
        if sala_existente:
            flash('Já existe uma sala com este número.', 'danger')
        else:
            nova_sala = Sala(
                numero=form.numero.data,
                capacidade=form.capacidade.data
            )
            db.session.add(nova_sala)
            db.session.commit()
            flash('Sala adicionada com sucesso!', 'success')
            return redirect(url_for('salas.listar_salas'))
    
    return render_template('adicionar_sala.html', form=form)

@salas.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_sala(id):
    sala = Sala.query.get_or_404(id)
    if not current_user.tipo == 'admin':
        flash('Acesso negado. Apenas administradores podem editar salas.', 'danger')
        return redirect(url_for('salas.listar_salas'))
    
    form = SalaForm(obj=sala)
    if form.validate_on_submit():
        sala.numero = form.numero.data
        sala.capacidade = form.capacidade.data
        db.session.commit()
        flash('Sala editada com sucesso!', 'success')
        return redirect(url_for('salas.listar_salas'))
    
    return render_template('editar_sala.html', form=form, sala=sala)

@salas.route('/excluir/<int:id>', methods=['POST'])
@login_required
def excluir_sala(id):
    sala = Sala.query.get_or_404(id)
    if not current_user.tipo == 'admin':
        flash('Acesso negado. Apenas administradores podem excluir salas.', 'danger')
        return redirect(url_for('salas.listar_salas'))

    db.session.delete(sala)
    db.session.commit()
    flash('Sala excluída com sucesso!', 'success')
    return redirect(url_for('salas.listar_salas'))
