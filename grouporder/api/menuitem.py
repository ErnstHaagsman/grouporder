from flask import request
from flask_restful import Resource, abort, reqparse

from api.users import login_required
from data.menuitems import MenuItem


class MenuItemApi(Resource):
    @login_required
    def put(self, restaurant_id, menu_item_id):
        if not request.user.can_manage_restaurants:
            abort(403, message="You do not have the necessary permissions")

        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, type=str,
                            help="The name of the menu item")
        parser.add_argument('price', required=True, type=float,
                            help="The price of the menu item")
        args = parser.parse_args()

        item = MenuItem.by_id(menu_item_id)
        item.update(args['name'], args['price'])

        return {
            'id': item.item_id,
            'name': item.name,
            'price': item.price
        }

    @login_required
    def delete(self, restaurant_id, menu_item_id):
        if not request.user.can_manage_restaurants:
            abort(403, message="You do not have the necessary permissions")

        item = MenuItem.by_id(menu_item_id)

        item.delete()