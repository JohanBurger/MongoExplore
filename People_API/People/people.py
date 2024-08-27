from flask import Blueprint, current_app, g, jsonify, make_response
from flask_pymongo import PyMongo, ObjectId

people = Blueprint('people', __name__, url_prefix='/people')

@people.route('/count', methods=['GET'])
def count():
    return 'Thirteen'

@people.route('/count', methods=['GET'])
def test():
    # TODO Factor out DB stuff
    db = getattr(g, '_db', None)
    if db is None:
        db = g._db = PyMongo(current_app).db

    collection = db['test_docker']
    return str(collection.count_documents({}))

@people.route('/<id>', methods=['GET'])
def get(id):
    db = getattr(g, '_db', None)
    if db is None:
        db = g._db = PyMongo(current_app).db

    # TODO - Add error handling
    collection = db['test_docker']
    id = ObjectId(id)
    person = collection.find({'_id': id}).next()
    if person is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(str(person))

