from flask import Flask
from People.people import people

def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['MONGO_URI'] = 'mongodb://app_user:app_user_password@localhost:27017/explore-db'
    app.register_blueprint(people)

    @app.route('/', methods=['GET'])
    def get():
        return 'Hello World!'

    return app

if __name__ == '__main__':
   app = create_app()
   app.run()
