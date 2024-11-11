from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint
from .models import Reserva, Sala, Usuario  # Importando os modelos do arquivo models.py

db = SQLAlchemy()

reservas = Blueprint('reservas', __name__)

# Exemplo de rota para o blueprint reservas
@reservas.route('/')
def index():
    return "Reservas"