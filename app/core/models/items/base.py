import copy

from mongoengine import Document, QuerySet
from mongoengine.fields import DictField, FloatField, StringField

from app.core.utilities.common import document_to_dict


class ItemsQuerySet(QuerySet):

    def convert_dict(self, params_dict: dict):
        collection_name = 'parameters'
        res = {}
        for k in params_dict.keys():
            res[f'{collection_name}.{k}'] = params_dict[k]
        return res

    def filter_params(self, params_dict: dict):
        filter_dict = copy.deepcopy(params_dict)
        if 'amount' in filter_dict:
            del filter_dict['amount']
        if 'type' in filter_dict:
            del filter_dict['type']
        if 'part_name' in filter_dict:
            del filter_dict['part_name']
        if 'id' in filter_dict:
            query_filter = {'_id': filter_dict['id']}
        else:
            query_filter = self.convert_dict(filter_dict)
        return self.filter(__raw__=query_filter)


class BaseItem(Document):
    crm_parameters = {}
    not_zero_amount = {'amount': {'$not': {'$eq': 0}}}
    id = StringField(primary_key=True)
    category_id = StringField()
    parameters = DictField()
    amount = FloatField()
    type = StringField()
    name = StringField()
    price = FloatField()
    measure = StringField()

    meta = {'collection': 'items',
            'allow_inheritance': True, 'queryset_class': ItemsQuerySet,
            'indexes': [
                {'fields': ['$name'],
                 'default_language': 'english',
                 'name': 'search_idx',
                 # "_type": 1
                 }
            ]
            }

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        self.is_finish = False
        self.MeasureCode = '796'
        self.MeasureName = 'Штука'
        self.MeasureInt = 'PCE'
        self.MeasureText = 'штук'
        self.NomenclatureType = ''

    def get_safe(self) -> dict:
        res = document_to_dict(self)
        return res

    def get_selection_name(self) -> str:
        return f'base'
