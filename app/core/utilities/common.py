from typing import Optional, Union

from bson import ObjectId
from mongoengine import QuerySet, Document, DictField, GenericReferenceField, EmbeddedDocumentField, EmbeddedDocument


def queryset_to_list(qs: QuerySet):
    return [each.to_mongo().to_dict() for each in qs]


def document_to_dict(obj: Union[Document, EmbeddedDocument]):
    return obj.to_mongo().to_dict()


def get_id_safe_document(document):
    document = document_to_dict(document)
    document['_id'] = str(document['_id'])
    return document


def queryset_to_json(qs: QuerySet):
    res = "["
    for i in qs:
        res += f'{i.to_json()},'
    res += ']'
    return res
