from bson import ObjectId
from flask_login import UserMixin
from werkzeug.security import check_password_hash

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

    def save(self):
        q = {}
        if self._id is not None:
            q = {'_id': self._id}
        db.insert(users_collection, self.__get__())

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
