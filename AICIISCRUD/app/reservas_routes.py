from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import db, Reserva

reservas_bp = Blueprint('reservas', __name__)

@reservas_bp.route('/reservar_sala', methods=['GET', 'POST'])
def reservar_sala():
    if request.method == 'POST':
        sala_id = request.form.get('sala_id')
        usuario = request.form.get('usuario')
        inicio = request.form.get('inicio')
        fim = request.form.get('fim')

        # Verifica se todos os campos foram preenchidos
        if not sala_id or not usuario or not inicio or not fim:
            flash('Todos os campos são obrigatórios!', 'error')
            return redirect(url_for('reservas.reservar_sala'))

        try:
            # Criar nova reserva e salvar no banco
            nova_reserva = Reserva(sala_id=sala_id, usuario=usuario, inicio=inicio, fim=fim)
            db.session.add(nova_reserva)
            db.session.commit()

            flash('Reserva realizada com sucesso!', 'success')
            return redirect(url_for('reservas.listar_reservas'))  # Redireciona para a lista de reservas
        except Exception as e:
            db.session.rollback()  # Desfaz a sessão em caso de erro
            flash(f'Ocorreu um erro: {str(e)}', 'error')

    # Renderiza a página de formulário de reserva
    return render_template('reservar_sala.html')
