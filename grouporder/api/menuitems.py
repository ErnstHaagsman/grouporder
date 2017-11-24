from flask import request
from flask_restful import Resource, abort, reqparse

from grouporder.api.users import login_required
from grouporder.data.menuitems import MenuItem


class MenuItemsApi(Resource):
    def get(self, restaurant_id):
        items = MenuItem.list(restaurant_id)

        dicts = [{'id': elem.item_id,
                  'name': elem.name,
                  'price': elem.price} for elem in items]

        return dicts

    @login_required
    def post(self, restaurant_id):
        if not request.user.can_manage_restaurants:
            abort(403, message="You do not have the necessary permissions")

        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, type=str,
                            help="The name of the menu item")
        parser.add_argument('price', required=True, type=float,
                            help="The price of the menu item")
        args = parser.parse_args()

        item = MenuItem.create(restaurant_id, args['name'], args['price'])

        return {
            'id': item.item_id,
            'name': item.name,
            'price': item.price
        }