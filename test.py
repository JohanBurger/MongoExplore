import time
import urllib.parse

import requests
from faker import Faker
from pymongo import MongoClient


fake = Faker(['de_DE'])
def create_client() -> dict:
    rand = fake.random_int(0, 5)
    person = {"creation_date": fake.date(), 'name': fake.name(), 'age': fake.random_int(18, 80)}
    match rand:
        case 1:
            person['city'] = fake.city()
        case 2:
            person['phone'] = fake.phone_number()
        case 3:
            person['email'] = fake.company_email()
        case 4:
            person['job'] = fake.job()
        case 5:
            person['company'] = fake.company()
    return person

_collection = None
def get_collection():
    if not hasattr(get_collection, 'collection'):
        username = urllib.parse.quote('app_user')
        password = urllib.parse.quote('app_user_password')
        database_name = 'explore-db'
        uri = 'mongodb://%s:%s@localhost:27017/%s'
        client = MongoClient(uri % (username, password, database_name))
        db = client[database_name]
        get_collection._collection = db['test_docker']
    return get_collection._collection


def insert_database(person):
    collection = get_collection()
    return collection.insert_one(person)


# def find_database(id: str):
#     collection = get_collection()
#     return collection.find_one({'_id': ObjectId(id)})


def insert_api(person: dict):
    url = 'http://localhost:5000/people/'
    files = {'image': open('feels-good-man.jpg', 'rb')}
    payload = person
    tic = time.perf_counter()
    response = requests.post(url, data = payload, files = files, )
    toc = time.perf_counter()
    print(f"Time taken: {toc - tic:0.4f} seconds")
    if response.ok:
        print(response.json())


if __name__ == '__main__':
    try :
        # collection.drop()
        for _ in range(1):
            client = create_client()
            # result = insert_database(client)
            result = insert_api(client)

        # print('Data inserted')
        # record_count = collection.count_documents({})
        # print(f'Total records in collection: {record_count}')
        #
        # record_with_company_count = collection.count_documents({'person.company': {'$exists': True}})
        # print(f'Total records with company: {record_with_company_count}')
        #
        # records = collection.find({'company': {'$exists': True}})
        # print(f'First record with company: {records.next()}')
        #
        # result = collection.insert_one(create_client())
        # print(result)
    except Exception as e:
        print()
        raise Exception('Caught the following exception: ', e)
