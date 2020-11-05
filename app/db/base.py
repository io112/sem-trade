from app.db import db
from pymongo import ReplaceOne, UpdateOne


def insert(collection, data):
    db[collection].insert(data)


def replace_upsert(collection, query, update):
    update: dict
    requests = [ReplaceOne(query, update, upsert=True)]
    db[collection].bulk_write(requests)


def update_upsert(collection, query, update):
    update: dict
    requests = [UpdateOne(query, update, upsert=True)]
    db[collection].bulk_write(requests)


def find_one(collection, query):
    return db[collection].find_one(query)


def find(collection, query):
    return db[collection].find(query)
