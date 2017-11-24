import os
import psycopg2
import simplejson as json
from flask import Flask, g, make_response
from flask_restful import Api

from grouporder.api.menuitem import MenuItemApi
from grouporder.api.menuitems import MenuItemsApi
from grouporder.api.restaurant import RestaurantApi
from grouporder.api.restaurants import RestaurantsApi
from grouporder.api.users import UsersApi, LoginApi

app = Flask(__name__)
api = Api(app)


api.add_resource(UsersApi, '/users')
api.add_resource(LoginApi, '/users/login')
api.add_resource(RestaurantsApi, '/restaurants')
api.add_resource(RestaurantApi, '/restaurant/<int:id>')
api.add_resource(MenuItemsApi, '/restaurant/<int:restaurant_id>/menu')
api.add_resource(MenuItemApi, '/restaurant/<int:restaurant_id>/menu/<int:menu_item_id>')

@api.representation('application/json')
def output_json(data, code, headers=None):
    json_string = json.JSONEncoder().encode(data)
    resp = make_response(json_string, code)
    resp.headers.extend(headers or {})
    return resp

@app.before_request
def before_request():
    g.db = psycopg2.connect(os.environ['DATABASE_URI'])

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')