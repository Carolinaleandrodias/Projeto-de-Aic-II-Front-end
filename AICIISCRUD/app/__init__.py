from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .models import db, Usuario 
from .usuarios import main as main_blueprint
from .usuarios import usuarios as usuarios_blueprint
#set FLASK_APP="__init__:create_app"
#flask run


def create_app():
    app = Flask(__name__, static_folder='static')
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SECRET_KEY'] = "212310"
    app.config['SQLALCHEMY_ECHO'] = True  # Da o log das queries no console

    # Inicializar banco de dados
    db.init_app(app)
    # db.create_all()
    print('initialize database')
    migrate = Migrate(app,db)
    login_manager = LoginManager(app)
    login_manager.login_view = 'usuarios.login'  # Redireciona usuários não logados para a rota de login
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))
    
    
    # Registrar blueprints
    app.register_blueprint(main_blueprint)
    app.register_blueprint(usuarios_blueprint, url_prefix='/usuarios')

    return app