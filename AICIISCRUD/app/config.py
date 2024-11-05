import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Usando SQLite em memória
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Desabilita notificações de mudanças para economizar recursos
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'uma_chave_secreta_default'  # Chave secreta para sessões
