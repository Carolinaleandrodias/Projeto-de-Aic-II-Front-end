import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'minha_chave_secreta'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Exemplo de URI para SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False


 