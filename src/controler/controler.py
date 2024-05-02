from flask import render_template, request, redirect,jsonify
from flask.views import MethodView
from src.db import  get_mysql_connection
from src.db import get_estados
import requests
import mysql.connector
from urllib.parse import urlparse,urlunparse
#from src.rosca import exibir_grafico_rosca
#from src.routes import *
#from src.routes.routes import get_routes

#from src.utils import cidadebyestado
from tkinter import messagebox

from flask.views import MethodView

class HomeController(MethodView):
    def get(self):
        # Lógica para manipular a requisição GET da rota /api/data
         return render_template('index.html')

 

class CadastrosController(MethodView):
    def get(self):
        estados = get_estados()
        
        return render_template('cadastro2.html', estados=estados)



    def post(self):
        try:
            connection = get_mysql_connection()
            name = request.form.get('nome')
            email = request.form.get('email')
            senha = request.form.get('senha')
            print(senha)
            telefone = request.form.get('telefone')
            sexo = request.form.get('sexo')
            estado = request.form.get('estado')
            cidade = request.form.get('cidade')
            date = request.form.get('date')
            confirm_value = request.form.get('confirm', 'off')
            confirm_int = 1 if confirm_value.lower() == 'on' else 0

               
            with connection.cursor() as cur:
               cur.execute("SELECT COUNT(*) FROM cadastro WHERE email = %s", (email,))
            if cur.fetchone()[0] > 0:
                    raise ValueError("E-mail já cadastrado")

            # Iniciar transação
            connection.begin()


            with connection.cursor() as cur:
                cur.execute("INSERT INTO cadastro (nome, email, telefone, sexo, estado, cidade, datanascimento, confirm) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                            (name, email, telefone, sexo, estado, cidade, date, confirm_int))
                connection.commit()

            with connection.cursor() as cur:
                cur.execute("INSERT INTO login (email,senha) VALUES (%s,%s)",
                            (email,senha))
                connection.commit()

      

        except Exception as e:
            error_message = "Erro ao cadastrar pessoa no banco de dados: " + str(e)
            return jsonify({'error': error_message}), 400


        finally:
            if connection:
                connection.close()
    
        return redirect('/cadastros')

    

class PerguntasController(MethodView):
    def get(self):
        #exibir_grafico_rosca(soma_respostas=100) 
        return render_template('perguntas.html')
     
class ResultadosController(MethodView):
    def get(self):
      #soma_respostas = request.args.get('soma')
    # Renderizar a página de resultados
      return render_template('resultados.html')

class LoginController(MethodView):
    def get(self):
        #soma_respostas = request.args.get('soma', '')
        return render_template('login.html')
    
class ResetController(MethodView):
    def get(self):
        return render_template('reset.html')
    

class CadastroController(MethodView):
    def get(self):
        return render_template('cadastro1.html')
    
class AgilController(MethodView):
    def get(self):
        return render_template('agil.html')
