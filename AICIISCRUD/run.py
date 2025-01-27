from app import create_app

app = create_app()  # Inicializa o Flask app

if __name__ == '__main__':
    # Start o Flask app com suporte a SSL
    app.run(debug=True, ssl_context=('cert.pem', 'key.pem'))
