import urllib.parse

from faker import Faker
from pymongo import MongoClient


fake = Faker(['de_DE'])
def create_client():
    rand = fake.random_int(0, 5)
    person = {}
    person["creation_date"] = fake.date()
    person['name'] = fake.name()
    person['age'] = fake.random_int(18, 80)
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


if __name__ == '__main__':
    username = urllib.parse.quote('app_user')
    password = urllib.parse.quote('app_user_password')
    database = 'explore-db'
    uri = 'mongodb://%s:%s@localhost:27017/%s'
    client = MongoClient(uri % (username, password, database))

    try :
        db = client[database]
        collection = db['test_docker']
        collection.drop()
        for _ in range(10_000):
            client = create_client()
            result = collection.insert_one(client)

        print('Data inserted')
        record_count = collection.count_documents({})
        print(f'Total records in collection: {record_count}')

        record_with_company_count = collection.count_documents({'person.company': {'$exists': True}})
        print(f'Total records with company: {record_with_company_count}')

        records = collection.find({'company': {'$exists': True}})
        print(f'First record with company: {records.next()}')

        result = collection.insert_one(create_client())
        print(result)
    except Exception as e:
        print()
        raise Exception('Caught the following exception: ', e)
