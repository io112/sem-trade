from mongoengine import Document, StringField, BooleanField, ValidationError

from app.core.utilities.common import document_to_dict


class Contragent(Document):
    name = StringField(required=True)
    surname = StringField()
    phone = StringField()
    inn = StringField()
    kpp = StringField()
    address = StringField(required=True)
    email = StringField(required=True)
    is_org = BooleanField(default=False)

    meta = {'indexes': [
        {'fields': ['$name', "$phone", '$surname'],
         'default_language': 'english',
         'name': 'search_idx',
         'weights': {'name': 1, 'phone': 1, 'surname': 1}
         }
    ]}

    def clean(self):
        if self.is_org:
            self.validate_org_part()
        else:
            self.validate_user_part()

    def validate_org_part(self):
        if not self.inn:
            raise ValidationError('ИНН не заполнен')
        if not self.kpp:
            raise ValidationError('КПП не заполнен')
        if len(self.inn) != 10:
            raise ValidationError('ИНН должен быть из 12 символов')
        if len(self.kpp) != 9:
            raise ValidationError('КПП должен быть из 9 символов')

    def validate_user_part(self):
        if not self.surname:
            raise ValidationError('Фамилия должна быть заполнена')

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
