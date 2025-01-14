import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///E:/planner-aic2/Projeto-de-Aic-II-Front-end/AICIISCRUD/app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Desabilita notificações de mudanças para economizar recursos
    SECRET_KEY = os.environ.get('SECRET_KEY') or '212310'  # Chave secreta para sessões

#sqlite3 E:/planner-aic2/Projeto-de-Aic-II-Front-end/AICIISCRUD/app.db
