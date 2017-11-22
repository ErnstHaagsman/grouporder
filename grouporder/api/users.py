from flask_restful import Resource, reqparse, abort

from grouporder.data.users import User, DuplicateUserError


class UsersApi(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True,
                            help='The desired username. Should be unique '
                                 'within the system')
        parser.add_argument('password', type=str, required=True,
                            help='Password, please pick something secure')
        parser.add_argument('fullname', type=str, required=True,
                            help='Your full name')
        parser.add_argument('email', type=str, required=True,
                            help='Your email address')
        args = parser.parse_args()

        try:
            new_user = User.create(args['username'],
                                   args['fullname'],
                                   args['email'],
                                   args['password'])
            return new_user.to_dict(), 201
        except DuplicateUserError:
            abort(409, message='A user with this username already exists')