import os
from datetime import datetime
from http import HTTPStatus

from flask import Blueprint, current_app, g, jsonify, make_response, request
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename

from People_API.People.db import get_person_by_id, create_person

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


@people.route('/<person_id>', methods=['GET'])
def get(person_id):
    person = get_person_by_id(person_id)
    if person is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(str(person))

# @people.route('/', methods=['POST'])
# def create():
#     person = request.json
#     # Validation here...
#     object_id = create_person(person)
#     if object_id is None:
#         return make_response(jsonify({'error': 'Not created'}), HTTPStatus.INTERNAL_SERVER_ERROR)
#     return make_response(jsonify({'_id': str(object_id)}), HTTPStatus.CREATED)

def create_timestamped_filename(filename):
    return f"{datetime.now().timestamp()}_{secure_filename(filename)}"

@people.route('/', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return make_response(jsonify({'error': 'No file part'}), HTTPStatus.BAD_REQUEST)
    file = request.files['image']
    if file.filename == '':
        return make_response(jsonify({'error': 'No selected file'}), HTTPStatus.BAD_REQUEST)
    # TODO More validation - check extension, size, etc.
    filename = create_timestamped_filename(file.filename)
    upload_folder = os.path.abspath(current_app.config['UPLOAD_FOLDER'])
    path = os.path.join(upload_folder, filename)
    file.save(path)

    person = request.form.to_dict()
    person["image_path"] = path
    object_id = create_person(person)
    if object_id is None:
        return make_response(jsonify({'error': 'Not created'}), HTTPStatus.INTERNAL_SERVER_ERROR)
    return make_response(jsonify({'_id': str(object_id)}), HTTPStatus.CREATED)
