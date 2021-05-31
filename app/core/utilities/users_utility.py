import secrets

from werkzeug.security import generate_password_hash

from app.core.models.user import User
from app.core.models.user_token import UserToken


def create_user_without_password(username, name, surname='', role='') -> UserToken:
    if check_username(username):
        raise ValueError('user with this username already exists')
    user = User()
    user.username = username
    user.password = generate_password_hash(secrets.token_hex(24))
    user.name = name
    user.surname = surname
    user.role = role
    user.save()
    token = UserToken(user=user)
    token.save()
    return token


def create_user(username, password, name, surname='', role='') -> User:
    if check_username(username):
        raise ValueError('user with this username already exists')
    user = User()
    user.username = username
    user.password = generate_password_hash(password)
    user.name = name
    user.surname = surname
    user.role = role
    user.save()
    return user


def change_password(user: User, password: str):
    if user.check_password(password):
        raise ValueError('Нельзя использовать старый пароль')
    user.password = generate_password_hash(password)
    user.change_password = False
    user.save()


def check_username(username):
    return User.objects(username=username).count() > 0
