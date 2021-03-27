from bson import ObjectId
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import base as db
from app.db.variables import users_collection


class User(UserMixin):
    def __init__(self):
        super().__init__()
        self._id = None
        self.password = ''
        self.username = ''
        self.name = ''
        self.surname = ''
        self.role = ''

    @staticmethod
    def get(uid):
        return User.create_from_db(db.find_one(users_collection, {'_id': ObjectId(uid)}))

    @staticmethod
    def get_by_username(username):
        return User.create_from_db(db.find_one(users_collection, {'username': username}))

    def get_id(self):
        return str(self._id)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def create_user(username, password, name, surname='', role=''):
        if User._check_username(username):
            raise ValueError('user with this username already exists')
        user = User()
        user.username = username
        user.password = generate_password_hash(password)
        user.name = name
        user.surname = surname
        user.role = role
        user._save()
        return user

    @staticmethod
    def _check_username(username):
        return len(db.find(users_collection, {'username': username})) > 0

    def _save(self):
        q = {}
        if self._id is not None:
            q = {'_id': self._id}
        id = db.insert(users_collection, self.__get__())
        self._id = id
        return id

    def __get__(self, instance=None, owner=None):
        res = {}
        for i, v in self.__dict__.items():
            if v is not None:
                res[i] = v
        return res

    @staticmethod
    def create_from_db(data):
        if data is None:
            return None
        user = User()
        for k, v in data.items():
            if k in user.__dict__:
                user.__dict__[k] = v
        return user
