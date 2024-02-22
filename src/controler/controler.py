from flask import render_template, request, redirect,jsonify
from flask.views import MethodView
from src.db import  get_mysql_connection
from src.db import get_estados
import mysql.connector
#from src.rosca import exibir_grafico_rosca
#from src.routes import *
#from src.routes.routes import get_routes

#from src.utils import cidadebyestado
from tkinter import messagebox

class HomeController(MethodView):
    def get(self):
        
            return render_template('home.html')
 

class CadastroController(MethodView):
    def get(self):
        estados = get_estados()
        
        return render_template('index.html', estados=estados)

    # Adicionando a rota para obter as cidades de um determinado estado


    def post(self):
        try:
            connection = get_mysql_connection()
            name = request.form.get('nome')
            email = request.form.get('email')
            telefone = request.form.get('telefone')
            sexo = request.form.get('sexo')
            estado = request.form.get('estado')
            cidade = request.form.get('cidade')
            date = request.form.get('date')
            confirm_value = request.form.get('confirm', 'off')
            confirm_int = 1 if confirm_value.lower() == 'on' else 0

            with connection.cursor() as cur:
                cur.execute("INSERT INTO cadastro (nome, email, telefone, sexo, estado, cidade, datanascimento, confirm) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                            (name, email, telefone, sexo, estado, cidade, date, confirm_int))
                connection.commit()

            with connection.cursor() as cur:
                cur.execute("INSERT INTO login (email) VALUES (%s)",
                            (email))
                connection.commit()

        except Exception as e:
            print(f"Erro ao cadastrar pessoa no banco de dados: {e}")
        finally:
            if connection:
                connection.close()

        return redirect('/cadastro')


    

class PerguntasController(MethodView):
    def get(self):
        #exibir_grafico_rosca(soma_respostas=100) 
        return render_template('perguntas.html')
     
class ResultadosController(MethodView):
    def get(self):
        return render_template('resultados.html')

class LoginController(MethodView):
    def get(self):
        return render_template('login.html')
    
class PloginController(MethodView):
    def get(self):
        return render_template('primeirologin.html')