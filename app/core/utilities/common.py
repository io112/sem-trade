from bson import ObjectId
from mongoengine import QuerySet, Document, DictField, GenericReferenceField, EmbeddedDocumentField


def queryset_to_list(qs: QuerySet):
    return [each.to_mongo().to_dict() for each in qs]


def document_to_dict(obj: Document):
    return obj.to_mongo().to_dict()


def get_id_safe_document(document):
    document = document_to_dict(document)
    document['_id'] = str(document['_id'])
    return document


def safe_introspect_object(document: Document) -> dict:
    res = {}
    obj_dict = document_to_dict(document)
    print(document.to_json())
    for key, val in document._fields.items():
        if val.__class__ is ObjectId:
            obj_dict[key] = str(val)
        elif val.__class__ is DictField:
            obj_dict[key] = _safe_introspect_dict(val)
        elif val.__class__ is GenericReferenceField:
            safe_introspect_object(val)
        elif val.__class__ is EmbeddedDocumentField:
            res[key] = safe_introspect_object(val)
        else:
            res[key] = val
    return obj_dict


def _safe_introspect_dict(doc_dict: dict) -> dict:
    return doc_dict


def queryset_to_json(qs: QuerySet):
    res = "["
    for i in qs:
        res += f'{i.to_json()},'
    res += ']'
    return res
