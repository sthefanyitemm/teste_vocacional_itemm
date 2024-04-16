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

    

    inteligenciac= f"INTELGIÊNCIA FÍSICO-CINESTÉTICA\n\nA Inteligência físico-cinestésica está presente em pessoas que possuem equilíbrio, velocidade, flexibilidade e expressão corporal. Sua principal habilidade é a capacidade de controlar os movimentos do corpo, coordenação motora fina e motora grossa. Dentre as profissões que se alinham a esse perfil estão: Atleta, dançarino(a), fisioterapeuta, cirurgião(ã), bombeiro(a), especialista em robótica, operador de máquinas CNC, técnico em manutenção de sistemas automatizados e mecânico industrial." 
    inteligenciae = f"INTELIGÊNCIA ESPACIAL\n\nA Inteligência Espacial está relacionada a pessoas com uma boa percepção visual e espacial, ou seja, com habilidade de interpretar e criar imagens através da cor, da forma e da textura. Essa inteligência pode ser definida como a capacidade de entender o mundo de forma tridimensional, física e mental. Sua maior habilidade é a criatividade. Dentre as profissões que se alinham a esse perfil estão: Arquitetos; Design Gráfico, Games e de Interiores; Esteticistas; Design de Moda; Jogos Digitais; Engenheiro de Produção; Fotógrafos; Astrônomos; Artes Visuais."
    inteligenciam = f"INTELIGÊNCIA LÓGICO-MATEMÁTICA\n\nA Inteligência Lógico-Matemática está ligada a capacidade que o ser humano tem para raciocínios dedutivos e conceitos matemáticos com elevada facilidade para resolver cálculos gerando destaque nas áreas de exatas e programação. Possuem também aptidão em resolução de problemas, da identificação de padrões e verificação de hipóteses.Dentre as profissões que se alinham a esse perfil estão: cientista, engenheiro(a), programador(a), matemático(a), analista financeiro(a), engenheiro de dados, cientista de dados, especialista em inteligência artificial e desenvolvedor de software. "
    inteligenciamu = f"INTELIGÊNCIA MUSICAL\n\nA Inteligência Musical demonstra grande habilidade de reconhecer, aprender, interpretar e diferenciar notas, timbres, melodias e ritmos. Essa inteligência está muito presente em pessoas que estão envolvidas com música, dança, artistas e produtores musicais. Dentre as profissões que se alinham a esse perfil estão:compositor(a), cantor(a), instrumentista, professor(a) de música, produtor(a) musical, engenheiro de som para produção audiovisual, desenvolvedor de software de música e especialista em experiência do usuário para plataformas de música online."
    inteligenciainter = f"INTELIGÊNCIA INTERPESSOAL\n\nA Inteligência Interpessoal está relacionada ao domínio da comunicação e persuasão. Pessoas com essa habilidade possui a facilidade de compreender o outro através do tom de voz e expressões faciais, além de possuir o poder de se expressar e interagir em público com facilidade. A empatia é uma das maiores qualidades dessa inteligência, assim como o espírito de liderança em situações em grupo. Dentre as profissões que se alinham a esse perfil estão: Gerente de Projetos; Psicólogos; Advogados; Assistentes Sociais; Médicos; Professores; Consultor de Negócios; Gestão de Recursos Humanos; Relações Públicas."
    inteligenciaintra = f"INTELIGÊNCIA INTRAPESSOA\n\nA inteligência intrapessoal está relacionada a pessoa que possui o autoconhecimento, ou seja, a conexão consigo mesmo. São pessoas que entendem seus próprios temperamentos, desejos, motivações e capacidades, usando-as em seu favor e bem-estar. Essa inteligência facilita a entrada da pessoa em qualquer campo profissional, pois ela beneficia suas relações sociais, levando-as a tomarem decisões certas e coerentes. As pessoas que possuem a inteligência intrapessoal são organizadas, ambiciosas com seus objetivos, disciplinadas e com alto foco e concentração nas atividades que realiza.Dentre as profissões que se alinham a esse perfil estão: Administração; Marketing; Coaching e Mentoring; Psicólogos Organizacionais; Jornalistas; Publicitários; Advogados; Assistente Sociais; Advogados."
    inteligencial = f"INTELIGÊNCIA LINGUÍSTICA\n\nA Inteligência Linguística está relacionada a pessoa que consegue se comunicar, aprender novas línguas e fazer uso da linguagem verbal e escrita de maneira diferenciada e tem domínio da língua de caráter morfológico, sintático e semântico. São pessoas com capacidade de persuasão.Dentre as profissões que se alinham a esse perfil estão: escritor(a), jornalista, advogado(a), professor(a) de línguas, tradutor(a), escritor técnico, redator de conteúdo digital, gerente de mídia social, especialista em SEO. "
    lgpd = f"Os dados coletados para uso neste teste vocacional estão em conformidade com a Lei 13.709/2018 (Lei Geral de Proteção de Dados - LGPD) e são essenciais para atingir a finalidade do tratamento.Maiores informações sobre o tratamento de dados realizados ITEMM, podem ser verificadas na Política de Privacidade, disponível em: (Políticas de Privacidade - ITEMM )Dúvidas, requerimentos ou ocorrências envolvendo o tratamento de dados pessoais ou qualquer incidente de segurança devem ser endereçados à Encarregada pelo Tratamento de Dados Pessoais/DPO do ITEMM, através do e-mail: dpo@itemm.com.br."

# Formatar a string com os resultados e a mensagem sobre as 3 inteligências
    email_content = f"{mensagem_top_3}\n\nResultados:\n{resultados_str}\n\nSaiba mais sobre as os tipos de inteligência:\n\n{inteligenciac}\n\n{inteligenciae}\n\n{inteligenciam}\n\n{inteligenciamu}\n\n{inteligenciainter}\n\n{inteligenciaintra}\n\n{inteligencial}\n\n\n\n{lgpd}"

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
