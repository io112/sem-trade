from bson import ObjectId
from mongoengine import Document, StringField, BooleanField

import app.db.base as db
from app.core.utilities.common import document_to_dict
from app.db.variables import contragent_collection


class Contragent(Document):
    name = StringField()
    surname = StringField()
    phone = StringField()
    inn = StringField()
    kpp = StringField()
    address = StringField()
    is_org = BooleanField(default=False)

    meta = {'indexes': [
        {'fields': ['$name', "$phone", '$surname'],
         'default_language': 'english',
         'name': 'search_idx',
         'weights': {'name': 1, 'phone': 1, 'surname': 1}
         }
    ]}

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        self.__session = None

    def __get__(self, instance=None, owner=None) -> dict:
        res = {}
        for k, v in self.__dict__.items():
            if k[:11] != '_Contragent' and v is not None and v != '':
                res[k] = v
        return res

    def get_safe(self) -> dict:
        contragent = document_to_dict(self)
        contragent['_id'] = str(contragent['_id'])
        return contragent

    def get(self):
        res = self.__get__()
        res['_id'] = str(res['_id'])
        return res

    def get_name(self):
        name = self.name
        if not self.is_org:
            name += " " + self.surname
        return name

    def save_to_db(self):
        db.insert(contragent_collection, self.__get__())

    # def save_to_session(self, session=None):
    #     if self.__session is None and session is None:
    #         raise Exception('Session not defined')
    #     if self.__session:
    #         session = self.__session
    #     session.add_data({'contragent': self.__get__()})
    #     update_session(session)

    # @staticmethod
    # def create_from_session(session: Session):
    #     cont_data = session.data.get('contragent')
    #     if cont_data is None:
    #         raise NotImplementedError('Contragent not defined')
    #     contragent = Contragent.create_from_dict(cont_data)
    #     contragent.__session = session
    #     return contragent

    @staticmethod
    def create_by_id(c_id):
        res = db.find(contragent_collection, {'_id': ObjectId(c_id)})
        if len(res) == 0:
            raise Exception('Contragent not found')
        return Contragent.create_from_dict(res[0])

    @staticmethod
    def create_from_dict(data):
        contragent = Contragent()
        for k, v in data.items():
            if k in contragent.__dict__:
                contragent.__dict__[k] = v
        return contragent

    @staticmethod
    def create_from_form(data):
        contragent = Contragent()
        for i in data:
            i: dict
            key = i['name']
            val = i['value']
            if key == 'is_org':
                contragent.is_org = True
            elif key in contragent.__dict__:
                contragent.__dict__[key] = val
        if contragent._id:
            contragent._id = ObjectId(contragent._id)
        return contragent

    @staticmethod
    def find_contragents(q):
        res = db.find(contragent_collection, {'$text': {'$search': q}})
        conts = []
        for i in res:
            conts.append(Contragent.create_from_dict(i).get())
        return conts
