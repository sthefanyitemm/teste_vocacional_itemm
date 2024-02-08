from flask import render_template, request, redirect,jsonify
from flask.views import MethodView
from src.db import  get_mysql_connection
from src.db import get_estados
#from src.utils import cidadebyestado
from tkinter import messagebox

class HomeController(MethodView):
    def get(self):
        
            return ('Heloo')
 

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
                cur.execute("INSERT INTO pessoas (nome, email, telefone, sexo, estado, cidade, datanascimento, confirm) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                            (name, email, telefone, sexo, estado, cidade, date, confirm_int))
                connection.commit()

        except Exception as e:
            print(f"Erro ao cadastrar pessoa no banco de dados: {e}")
        finally:
            if connection:
                connection.close()

        return redirect('/cadastro')

"""
class PerguntasController(MethodView):
    def get(self):
         
          return render_template('perguntas.html')

def botao_clicado(valor):
    print(f"Botão {valor} clicado")
    messagebox.showinfo("Alerta", f"Botão {valor} clicado")

def criar_botoes(root):
    for i in range(7):
        botao = tk.Button(root, text=f"Botão {i}", command=lambda i=i: botao_clicado(i))
        botao.pack()

root = tk.Tk()
criar_botoes(root)
"""
