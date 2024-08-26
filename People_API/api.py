from flask import Flask
from People.people import people

def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['MONGO_URI'] = 'mongodb://app_user:app_user_password@localhost:27017/explore-db'
    app.config['UPLOAD_FOLDER'] = 'C:\\Users\\jdpbu\\Source\\Python-MongoDB\\MongoExplore\\images'
    app.register_blueprint(people)

    return app

if __name__ == '__main__':
   app = create_app()
   app.run()
