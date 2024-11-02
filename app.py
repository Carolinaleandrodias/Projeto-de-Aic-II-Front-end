from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

@app.route('/auth', methods = ['GET','POST'])
def auth():
    if request.method == 'POST':
        if 'login' in request.form:
            matricula = request.form['matricula']
            senha = request.form['senha']
            print(f"Matricula: {matricula}")
            print(f"Senha: {senha}")
            return redirect(url_for('agend'))
        
        elif 'request' in request.form:
            nome_cad = request.form['nome_cad']
            data_cad = request.form['data_cad']
            email_cad = request.form['email_cad']
            matricula_cad = request.form['matricula_cad']
            senha_cad = request.form['senha_cad']
            
            print(f"nome: {nome_cad}")
            print(f"data: {data_cad}")
            print(f"email: {email_cad}")
            print(f"matricula: {matricula_cad}")
            print(f"senha: {senha_cad}")
            return redirect(url_for('auth'))
    return render_template('index.html')

@app.route('/agendamento')
def agend():
    return render_template('agenda.html')



if __name__ == '__main__':
    app.run(debug=True)