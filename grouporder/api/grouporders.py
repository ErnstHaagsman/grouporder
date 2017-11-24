import dateutil.parser as date_parser
from flask import request
from flask_restful import Resource, reqparse

from api.users import login_required
from data.orders import Order


class GroupOrdersApi(Resource):
    def get(self):
        current_orders = Order.list_current()

        dicts = []
        for order in current_orders:
            dicts.append({
                'id': order.order_id,
                'restaurant_id': order.restaurant_id,
                'restaurant': order.restaurant_name,
                'organizer': order.organizer,
                'time': order.order_time
            })

        return dicts

    @login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('restaurant_id', type=int, required=True,
                            help="From which restaurant would you like to order?")
        parser.add_argument('order_time', type=lambda x: date_parser.parse(x),
                            required=True,
                            help="When would you like to place the order?")
        args = parser.parse_args()

        order = Order.create(request.user.username,
                             args['restaurant_id'],
                             args['order_time'])

        return {
            'id': order.order_id,
            'restaurant_id': order.restaurant_id,
            'restaurant': order.restaurant_name,
            'organizer': order.organizer,
            'time': order.order_time
        }, 201