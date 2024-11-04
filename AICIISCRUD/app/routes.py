from flask import Blueprint, render_template, request, redirect, url_for
from .models import models_sql_db as db, Sala
from flask import flash
main = Blueprint('main', __name__)

@main.route('/listar_salas')
def listar_salas():
    salas = Sala.query.all()
    return render_template('listar_salas.html', salas=salas)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/registrar_sala', methods=['GET', 'POST'])

def registrar_sala():
    try:
        if request.method == 'POST':
            nome = request.form['nome']
            nova_sala = Sala(nome=nome)
            db.session.add(nova_sala)
            db.session.commit()
            flash('Sala criada com sucesso!', 'success')
            return redirect(url_for('main.listar_salas'))
        return render_template('registrar_sala.html')
    except Exception as e:
        return str(e)