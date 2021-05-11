from mongoengine import QuerySet, Document


def queryset_to_list(qs: QuerySet):
    return [each.to_mongo().to_dict() for each in qs]


def document_to_dict(obj: Document):
    return obj.to_mongo().to_dict()
