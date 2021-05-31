from bson import ObjectId
from flask_login import UserMixin
from mongoengine import Document, StringField, BooleanField
from werkzeug.security import check_password_hash, generate_password_hash

from app.core.utilities.common import document_to_dict


class User(UserMixin, Document):
    password = StringField()
    username = StringField()
    name = StringField()
    surname = StringField()
    change_password = BooleanField(default=True)
    role = StringField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_safe(self) -> dict:
        res = document_to_dict(self)
        res['_id'] = str(res['_id'])
        return res

    @staticmethod
    def get(uid):
        return User.objects(id=ObjectId(uid)).first()

    @staticmethod
    def get_by_username(username):
        return User.objects(username=username)[0] if User.objects(username=username).count() > 0 else None

    def get_id(self):
        return str(self.id)

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
        user.save()
        return user

    @staticmethod
    def _check_username(username):
        return User.objects(username=username).count() > 0

    # def _save(self):
    #     q = {}
    #     if self._id is not None:
    #         q = {'_id': self._id}
    #     id = db.insert(users_collection, self.__get__())
    #     self._id = id
    #     return id
    #
    # def __get__(self, instance=None, owner=None):
    #     res = {}
    #     for i, v in self.__dict__.items():
    #         if v is not None:
    #             res[i] = v
    #     return res
    #
    # @staticmethod
    # def create_from_db(data):
    #     if data is None:
    #         return None
    #     user = User()
    #     for k, v in data.items():
    #         if k in user.__dict__:
    #             user.__dict__[k] = v
    #     return user
