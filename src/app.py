from flask import Flask,render_template,jsonify, request
from brasilapy import BrasilAPI
from src.routes.routes import *
from src.utils import *
from brasilapy.constants import IBGEProvider
from brasilapy.exceptions import ProcessorException
from src.controler import *
from flask_wtf import FlaskForm
from wtforms import SelectField
from flask_mysqldb import MySQL,MySQLdb
from src.db import *
#from src.db import get_estados



app = Flask(__name__,template_folder='templates')






@app.route('/cidade/<get_cidade>')
def statebycountry(get_cidade):
    connection = get_mysql_connection()
    with connection.cursor() as cur:
        result = cur.execute("SELECT * FROM cidade where CT_UF = %s",[get_cidade])
        print(f"Resultado da consulta SQL: {result}")
        cidade = cur.fetchall()
        print(f"Registros da cidade: {cidade}")
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
#app.add_url_rule('/perguntas', view_func=PerguntasController.as_view('perguntas'))
app.add_url_rule('/cidades', view_func=CadastroController.as_view('obter_cidades'))

