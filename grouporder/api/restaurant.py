from flask import request, abort
from flask_restful import reqparse, Resource

from api.users import login_required
from data.restaurants import Restaurant, DuplicateRestaurantNameError


class RestaurantApi(Resource):
    def get(self, id):
        restaurant = Restaurant.by_id(id)

        return {
            'id': restaurant.id,
            'name': restaurant.name
        }

    @login_required
    def put(self, id):
        if not request.user.can_manage_restaurants:
            abort(403, message="You do not have the necessary permissions")

        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, type=str,
                            help="The name of the restaurant")
        args = parser.parse_args()

        try:
            restaurant = Restaurant.by_id(id)
            restaurant.rename(args['name'])
        except DuplicateRestaurantNameError:
            abort(409, message='There is already a restaurant with this name')

        return {
            'id': restaurant.id,
            'name': args['name']
        }