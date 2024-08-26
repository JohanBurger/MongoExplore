from flask import g, current_app
from flask_pymongo import ObjectId, PyMongo
from werkzeug.local import LocalProxy


def get_db():
    db = getattr(g, '_db', None)
    if db is None:
        db = g._db = PyMongo(current_app).db
    return db

db = LocalProxy(get_db)

def get_person_by_id(person_id):
    try:
        collection = db['test_docker']
        object_id = ObjectId(person_id)
        return collection.find({'_id': object_id}).next()

    # TODO Better exception handling
    except Exception as e:
        print(e)
        return None

def create_person(person):
    try:
        collection = db['test_docker']
        result = collection.insert_one(person)
        return result.inserted_id
    except Exception as e:
        print(e)
        return None