from flask import Flask,render_template,jsonify, request
import matplotlib.pyplot as plt
import io
import base64
from src.routes.routes import *
from src.controler import *
from src.db import *
from src.utils.sendmail import send_email
import pymysql.cursors
from flask import redirect
from urllib.parse import urlparse,urlunparse
from flask import Blueprint
#from src.routes import api_blueprint




app = Flask(__name__,template_folder='templates')



@app.route('/send_email', methods=['POST'])
def send_email_route():
    data = request.get_json()
    email = data.get('email')
    send_email(email)
    return jsonify({"message": "Um link para criação/redefinição de senha foi enviado para o seu e-mail."})


@app.route('/cidade/<get_cidade>')
def statebycountry(get_cidade):
    connection = get_mysql_connection()
    with connection.cursor() as cur:
        result = cur.execute("SELECT * FROM cidade where CT_UF = %s",[get_cidade])
        cidade = cur.fetchall()
        cidadeArray = []
        for row in cidade:
            cidadeObj = {
                'id': row[0],   # Assumindo que CT_ID é a primeira coluna na sua consulta SQL
                'name': row[1]  # Assumindo que CT_NOME é a segunda coluna na sua consulta SQL
                        }
            cidadeArray.append(cidadeObj)
    return jsonify({'cidadeestado': cidadeArray})


@app.route('/verificar_senha', methods=['POST'])
def verificar_senha():
    # Obter os dados do formulário
    senha_digitada = request.form['senha']
    email = request.form['email']
    
    # Conectar ao banco de dados
    connection = pymysql.connect(host='localhost', port=3306, user='root', passwd='Itemm@', database='teste_prod')

    try:
        with connection.cursor() as cursor:
        # Consulta SQL para obter a senha armazenada no banco de dados
            sql = "SELECT senha, email FROM login WHERE email = %s"
            cursor.execute(sql, (email,))
            result = cursor.fetchone()

            if result:
                senha_banco = result[0]  # Acessar a senha pelo índice da coluna na tupla

            # Comparar a senha digitada com a senha do banco de dados
                if senha_digitada != senha_banco:
                # Senha incorreta, retornar mensagem de erro
                    return "Erro: Senha incorreta."
                else:
                # Senha correta, conceder acesso
                    #return "Senha correta. Acesso concedido."
                 return "Senha correta. Acesso concedido."
                 
                
                
            else:
            # Usuário não encontrado, retornar mensagem de erro
                return "Erro: Usuário não encontrado."

    finally:
    # Fechar conexão com o banco de dados
        connection.close()






app.add_url_rule(routes["home"], view_func=HomeController.as_view('home'))
app.add_url_rule(routes["cadastro"], view_func=CadastroController.as_view('cadastro'))
app.add_url_rule('/perguntas', view_func=PerguntasController.as_view('perguntas'))
app.add_url_rule('/cidades', view_func=CadastroController.as_view('obter_cidades'))
app.add_url_rule('/resultados', view_func=ResultadosController.as_view('resultados'))
app.add_url_rule('/login', view_func=LoginController.as_view('login'))
app.add_url_rule('/reset', view_func=ResetController.as_view('reset'))
