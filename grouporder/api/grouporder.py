from flask import request
from flask_restful import Resource, reqparse

from api.users import login_required
from data.lineitems import LineItem
from data.orders import Order


class GroupOrderApi(Resource):
    @login_required
    def get(self, order_id):
        order = Order.by_id(order_id)

        if request.user.username == order.organizer:
            items = order.get_all_items()
        else:
            items = order.get_items_for_user(request.user.username)

        return {
            'id': order.order_id,
            'restaurant_id': order.restaurant_id,
            'restaurant': order.restaurant_name,
            'organizer': order.organizer,
            'time': order.order_time,
            'items': items
        }

    @login_required
    def post(self, order_id):
        parser = reqparse.RequestParser()
        parser.add_argument('menu_item_id', type=int, required=True,
                            help="Please specify the menu item")
        args = parser.parse_args()

        item = LineItem.create(request.user.username, order_id, args['menu_item_id'])

        return {
            'menu_item_id': item.menu_item_id
        }
