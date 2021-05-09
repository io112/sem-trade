from urllib.parse import quote_plus
from app.constants import db_name, db_login, db_password, db_host

from pymongo import MongoClient
from mongoengine import connect, register_connection


uri = f"mongodb://%s:%s@%s/%s" % (
    quote_plus(db_login),
    quote_plus(db_password),
    quote_plus(db_host),
    quote_plus(db_name))
client = MongoClient(uri)
db = client[db_name]


def init():
    global uri, client, db
    uri = f"mongodb://%s:%s@%s/%s" % (
        quote_plus(db_login),
        quote_plus(db_password),
        quote_plus(db_host),
        quote_plus(db_name))
    client = MongoClient(uri)
    connect(db=db_name, username=db_login, password=db_password, host=db_host)
    db = client[db_name]
