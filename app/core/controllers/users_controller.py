from typing import Optional

from app.core.controllers import mail_controller
from app.core.models.user import User
from app.constants import root_password, root_username
from app.core.models.user_token import UserToken
from app.core.utilities import users_utility as utility
from datetime import datetime, timedelta

token_timeout = timedelta(days=3)


def check_super_user():
    if User.objects(username=root_username).count() == 0:
        utility.create_user(root_username, root_password, 'root', role='super_admin')


def login_using_token(token: str) -> Optional[User]:
    user_tokens = UserToken.objects(token=token)
    if user_tokens.count() == 0:
        return None
    user_token = user_tokens.first()
    if (datetime.now() - user_token.created_at) > token_timeout:
        user_token.delete()
        return None
    user = user_token.user
    return user


def create_user(**kwargs):
    if User.objects(username=kwargs['username']).count() > 0:
        raise ValueError('Пользователь уже существует')
    token = utility.create_user_without_password(**kwargs)
    mail_controller.send_user_created_email(token)
    return token


def change_password(**kwargs):
    password = kwargs['password']
    confirm_password = kwargs['confirm_password']
    user = kwargs['user']
    if password != confirm_password:
        raise ValueError('Пароли не совпадают')
    if len(password) < 8:
        raise ValueError('Пароль должен быть длинее 8 символов')
    else:
        utility.change_password(user, password)
        UserToken.objects(user=user.id).delete()
    return user
