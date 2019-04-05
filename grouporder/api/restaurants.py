from flask import request
from flask_restful import Resource, abort, reqparse

from api.users import login_required
from data.restaurants import Restaurant, DuplicateRestaurantNameError


class RestaurantsApi(Resource):
    @login_required
    def post(self):
        if not request.user.can_manage_restaurants:
            abort(403, message="You do not have the necessary permissions")

        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, type=str,
                            help="The name of the restaurant")
        args = parser.parse_args()
        name = args['name']

        try:
            new_restaurant = Restaurant.create(name)
        except DuplicateRestaurantNameError:
            abort(409, message=f'There is already a restaurant named {name}')

        return {
            'id': new_restaurant.id,
            'name': new_restaurant.name
        }, 201

    def get(self):
        restaurants = Restaurant.list()

        dicts = [{'id': elem.id, 'name': elem.name} for elem in restaurants]

        return dicts
