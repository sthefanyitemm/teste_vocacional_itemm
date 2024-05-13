from flask import Flask,render_template,jsonify, request
import matplotlib.pyplot as plt
import json
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
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify
from flask_cors import CORS
import re





app = Flask(__name__,template_folder='templates')
CORS(app)


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



def enviar_resultados_por_email(email, resultadosTexto):
    # Configurar informações do e-mail
    sender_email = 'sthefany.lima@itemm.com.br'  # Substitua pelo seu endereço de e-mail
    subject = 'Resultados do teste vocacional'
    message = resultadosTexto 

    # Configurar o corpo do e-mail
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    # Configurar servidor SMTP
    smtp_server = 'smtp.office365.com'
    smtp_port = 587
    smtp_username = 'sthefany.lima@itemm.com.br'
    smtp_password = '!@Devpy0'
    
    try:
        # Iniciar conexão com o servidor SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        # Enviar e-mail
        server.sendmail(sender_email, email, msg.as_string())

        # Encerrar conexão com o servidor SMTP
        server.quit()

        return True  # Email enviado com sucesso
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        return False  # Falha ao enviar o email



def enviar_resultados_por_email(email, resultadosTexto):
    # Configurar informações do e-mail
    sender_email = 'testevocacional@itemm.com.br'  # Substitua pelo seu endereço de e-mail
    subject = 'Resultados do teste vocacional'
    message = resultadosTexto 

    # Configurar o corpo do e-mail
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    # Configurar servidor SMTP
    smtp_server = 'smtp.office365.com'
    smtp_port = 587
    smtp_username = 'testevocacional@itemm.com.br'
    smtp_password = 'Itemm@2024'
    
    try:
        # Iniciar conexão com o servidor SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        # Enviar e-mail
        server.sendmail(sender_email, email, msg.as_string())

        # Encerrar conexão com o servidor SMTP
        server.quit()

        return True  # Email enviado com sucesso
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        return False  # Falha ao enviar o email


@app.route('/enviar_resultados_por_email', methods=['POST'])
def enviar_email():
    # Obter os dados do email do corpo da solicitação
    data = request.json
    email = data.get('email')
    resultadosTexto = data.get('resultadosTexto') 

    # Se estiver enviando dados JSON
    if email is None or resultadosTexto is None:
        return jsonify({'error': 'Campos de dados ausentes'}), 400
    
    # Converter a string JSON em um dicionário Python
    resultados_dict = json.loads(resultadosTexto)

    # Ordenar o dicionário em ordem decrescente com base nos valores
    resultados_ordenados = sorted(resultados_dict.items(), key=lambda x: x[1], reverse=True)

    # Inicializar uma lista para armazenar as 3 inteligências com os maiores valores
    top_3_inteligencias = []

    # Inicializar uma string para armazenar os resultados formatados
    resultados_str = ""

    # Formatar a string com os resultados ordenados e encontrar as 3 inteligências com os maiores valores
    for chave, valor in resultados_ordenados:
        resultados_str += f"{chave}: {valor}\n"
        top_3_inteligencias.append(chave)
        if len(top_3_inteligencias) == 3:
            break

    # Mensagem sobre as 3 inteligências com maiores valores
    mensagem_top_3 = f"As 3 inteligências que apresentaram maiores valores são: {', '.join(top_3_inteligencias)}"

    # Formatar a string com os resultados e a mensagem sobre as 3 inteligências
    email_content = f"{mensagem_top_3}\n\nResultados:\n{resultados_str}\n\nSaiba mais sobre as os tipos de inteligência:\n\n"

    # Enviar email
    if enviar_resultados_por_email(email, email_content):
        return jsonify({'message': 'Email enviado com sucesso!'}), 200
    else:
        return jsonify({'error': 'Erro ao enviar o email. Por favor, tente novamente mais tarde.'}), 500


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
                if senha_digitada == senha_banco:
                    # Senha correta, conceder acesso
                    return "Senha correta. Acesso concedido."
                else:
                    # Senha incorreta, retornar mensagem de erro
                    return "Erro: Senha incorreta."
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
app.add_url_rule('/cadastros', view_func=CadastrosController.as_view('cadastros'))
app.add_url_rule('/agil', view_func=AgilController.as_view('agil'))