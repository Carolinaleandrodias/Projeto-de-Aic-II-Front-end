from flask import Flask, render_template, url_for, request, redirect, send_from_directory, flash
import os, json

app = Flask(__name__)
app.secret_key = os.urandom(24)

logado = False

@app.route('/auth', methods = ['GET','POST'])
def auth():
    global logado 
    
    #print('request.form',request.form)
   

    if request.method == 'POST':
        if 'login' in request.form:
            #matricula = request.form['matricula']
            #senha = request.form['senha']
            # print(f"Matricula: {matricula}")
            # print(f"Senha: {senha}")
            matricula = request.form.get('matricula')
            senha = request.form.get('senha')
            
            # Abre o arquiv json.
            with open('usuarios.json') as usuariosTemp:
                usuarios = json.load(usuariosTemp)

            cont = 0
            for usuario in usuarios:
                cont += 1
                if matricula == 'adm' and senha == '000':
                    logado = True
                    return redirect(url_for('agend'))

                if usuario['matricula'] == matricula and usuario['senha'] == senha:
                    logado = True
                    return redirect(url_for('agend'))

                if cont >= len(usuarios):
                      flash('USUÁRIO INVÁLIDO!')
                      return redirect('/auth')
            # if matricula == '119847' and senha == '123':
            #     return redirect(url_for('agend'))
            # else:
            #     flash('USUÁRIO INVÁLIDO!')
            #     return redirect('/auth')

        
        elif 'register' in request.form:
            user = []
            nome = request.form.get('nome')
            data = request.form.get('data')
            email = request.form.get('email')
            matricula = request.form.get('matricula')
            senha = request.form.get('senha')
                
            user = [
                {
                    'nome': nome,
                    'data': data,
                    'email': email,
                    'matricula': matricula,
                    'senha': senha
                }
            ]

            with open('usuarios.json') as usuariosTemp:
                usuarios = json.load(usuariosTemp)

            usuarioNovo = user + usuarios

            with open ('usuarios.json','w') as gravarTemp:
                json.dump(usuarioNovo, gravarTemp, indent=4)

            # nome_cad = request.form['nome_cad']
            # data_cad = request.form['data_cad']
            # email_cad = request.form['email_cad']
            # matricula_cad = request.form['matricula_cad']
            # senha_cad = request.form['senha_cad']            
            # print(f"nome: {nome_cad}")
            # print(f"data: {data_cad}")
            # print(f"email: {email_cad}")
            # print(f"matricula: {matricula_cad}")
            # print(f"senha: {senha_cad}")
            
           
            return redirect(url_for('auth'))

    return render_template('index.html')

@app.route('/agendamento')
def agend():

    if logado == False:
        return redirect('/auth')
    
    if logado == True:
        return render_template('agenda.html')

# @app.route('/dados/salas.json')
# def get_salas():
#     return send_from_directory('static', 'salas.json')


if __name__ == '__main__':
    app.run(debug=True)