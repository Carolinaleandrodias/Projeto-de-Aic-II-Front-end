from flask import Flask
from flask import Blueprint
from .routes import main
from .reservas_routes import reservas_bp
from flask_sqlalchemy import SQLAlchemy
from .database import sql_db


def create_app():
    app = Flask(__name__)

    # Configurações do banco de dados e outras configurações aqui
    try:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        sql_db.init_app(app)

        # Registrando blueprints
        if isinstance(main, Blueprint):
            app.register_blueprint(main)
        else:
            raise ValueError("Blueprint 'main' is not a valid Blueprint instance")

        if isinstance(reservas_bp, Blueprint):
            app.register_blueprint(reservas_bp, url_prefix='/reservas')
        else:
            raise ValueError("Blueprint 'reservas_bp' is not a valid Blueprint instance")

    except Exception as e:
        # Log the exception or handle it accordingly
        print(f"An error occurred during app creation: {e}")
        raise AppCreationError(f"Failed to create app: {e}") from e

    return app


class AppCreationError(Exception):
    pass