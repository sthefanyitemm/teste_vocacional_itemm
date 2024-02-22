from flask import Flask,render_template,jsonify, request
import matplotlib.pyplot as plt
import io
import base64
from src.routes.routes import *
from src.controler import *
from src.db import *
from src.utils.sendmail import send_email



app = Flask(__name__,template_folder='templates')

@app.route('/salvar_respostas', methods=['POST'])
def salvar_respostas():
    resposta = int(request.json.get('resposta'))
    # Aqui você pode calcular os valores apropriados para o gráfico de rosca com base na resposta
    # Por enquanto, usaremos uma lista de valores fixos para demonstração
    valores = [10, 20, 30]
    perguntas = ['Pergunta 1', 'Pergunta 2', 'Pergunta 3']
    
    # Exibir o gráfico de rosca
    fig, ax = plt.subplots()
    ax.pie(valores, labels=perguntas, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # Salvar a imagem do gráfico em memória
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    # Converter a imagem em formato base64 para ser exibida no HTML
    grafico_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close(fig)  # Fechar a figura para liberar a memória
    return 'data:image/png;base64,' + grafico_base64

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




app.add_url_rule(routes["home"], view_func=HomeController.as_view('home'))
app.add_url_rule(routes["cadastro"], view_func=CadastroController.as_view('cadastro'))
app.add_url_rule('/perguntas', view_func=PerguntasController.as_view('perguntas'))
app.add_url_rule('/cidades', view_func=CadastroController.as_view('obter_cidades'))
app.add_url_rule('/resultados', view_func=ResultadosController.as_view('resultados'))
app.add_url_rule('/login', view_func=LoginController.as_view('login'))
app.add_url_rule('/plogin', view_func=PloginController.as_view('plogin'))