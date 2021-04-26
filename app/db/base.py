from typing import Dict

from app.db import db
from pymongo import ReplaceOne, UpdateOne


def insert(collection, data):
    return db[collection].insert_one(data).inserted_id


def replace_upsert(collection, query, update_data):
    update_data: dict
    requests = [ReplaceOne(query, update_data, upsert=True)]
    db[collection].bulk_write(requests)


def replace(collection, query, update_data, upsert=False):
    update_data: dict
    requests = [ReplaceOne(query, update_data, upsert=upsert)]
    db[collection].bulk_write(requests)


def update_upsert(collection, query, update_data: dict):
    update(collection, query, update_data, True)


def update(collection, query, update_data: dict, upsert=False):
    requests = [UpdateOne(query, update_data, upsert=upsert)]
    db[collection].bulk_write(requests)


def find_one(collection, query,fields=None, sorting=None):
    if sorting is None:
        sorting = []
    return db[collection].find_one(query, fields, sort=sorting)


def find(collection, query, fields=None, sorting=None):
    if sorting is None:
        sorting = []
    if query is None:
        query = {}
    resp = db[collection].find(query, fields, sort=sorting)
    result = []
    for i in resp:
        result.append(i)
    return result


def join_queries(*queries):
    res = {}
    for i in queries:
        if not isinstance(i, dict):
            continue
        res.update(i)
    return res


def join_queries_and_find(collection, *queries):
    return find(collection, join_queries(*queries))


def distinct_find(collection, query):
    if query is None:
        query = {}
    resp = db[collection].find(query)
    for i in query:
        resp = resp.distinct(i)
    result = []
    for i in resp:
        result.append(i)
    return result


def remove(collection, query):
    return db[collection].delete_one(query)
