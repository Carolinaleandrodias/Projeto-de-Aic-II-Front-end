from app import create_app

app = create_app()  # Initialize the Flask app

if __name__ == '__main__':
    app.run(debug=True)  # Start the Flask app