from flask import Flask
from flask_login import LoginManager
from .routes import main as main_blueprint
from .config import Config
from .models import db, Usuario 
from .reservas import reservas as reservas_blueprint
from .salas import salas as salas_blueprint
from .usuarios import usuarios as usuarios_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = "212310"

    # Inicializar banco de dados
    db.init_app(app)
    login_manager = LoginManager(app)
    login_manager.login_view = 'usuarios.login'  # Redireciona usuários não logados para a rota de login
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))
    
    
    # Registrar blueprints
    app.register_blueprint(main_blueprint)
    app.register_blueprint(usuarios_blueprint, url_prefix='/usuarios')
    app.register_blueprint(reservas_blueprint, url_prefix='/reservas')
    app.register_blueprint(salas_blueprint, url_prefix='/salas')  

    return app