import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(receiver_email):
    # Configurar informações do e-mail
    sender_email = 'testevocacional@itemm.com.br'
    subject = 'teste send email '
    message = 'Um link para criação de senha foi enviado para o seu e-mail.'

    # Configurar o corpo do e-mail
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    # Configurar servidor SMTP
    smtp_server = 'smtp.office365.com'
    smtp_port = 587
    smtp_username = 'testevocacional@itemm.com.br'
    smtp_password = 'Itemm@2024'

    # Iniciar conexão com o servidor SMTP
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)

    # Enviar e-mail
    server.sendmail(sender_email, receiver_email, msg.as_string())

    # Encerrar conexão com o servidor SMTP
    server.quit()
