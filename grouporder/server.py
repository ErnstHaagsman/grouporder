import os
import psycopg2
from flask import Flask, g
from flask_restful import Api

from grouporder.api.users import UsersApi

app = Flask(__name__)
api = Api(app)


api.add_resource(UsersApi, '/users')

@app.before_request
def before_request():
    g.db = psycopg2.connect(os.environ['DATABASE_URI'])

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')