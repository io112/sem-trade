from app.constants import *
from app.core.models.user_token import UserToken
from app.core.utilities import mail_utility as utility


def send_user_created_email(user_token: UserToken):
    user = user_token.user
    link = f'{current_host}?token={user_token.token}'
    uname = user.name + (' ' + user.surname) if user.surname else ''
    text = f'Здравствуйте, {uname}! Для этого адреса создан аккаунт в программе РВД. ' \
           f'Перейдите по ссылке для завершения регистрации: {link}.\n' \
           f'Ссылка действительна три дня.'
    utility.send_mail(user.username, 'Регистрация РВД', text)
