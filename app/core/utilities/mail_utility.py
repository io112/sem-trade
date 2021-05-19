import smtplib, ssl
from email.header import Header
from email.mime.text import MIMEText

from app.constants import *

header_text = f'RVD instance: {current_instance}\n' \
              f'Это письмо сгенерировано автоматически программой РВД' \
              f'\n--\n'
context = ssl.create_default_context()


def send_mail(to: str, subject: str, text: str):
    text = f'{header_text}{text}'
    msg = MIMEText(text, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = mail_username
    msg['To'] = to
    with smtplib.SMTP_SSL(mail_server, mail_port, context=context) as server:
        server.command_encoding = 'utf-8'
        server.login(mail_username, mail_password)
        server.sendmail(mail_username, to, msg.as_string())
