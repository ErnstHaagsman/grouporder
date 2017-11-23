import base64
from flask import request
from functools import wraps

from flask_restful import Resource, reqparse, abort

from grouporder.data.users import User, DuplicateUserError, login


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
            return {
                        'username': new_user.username,
                        'fullname': new_user.fullname,
                        'email': new_user.email
                   }, 201
        except DuplicateUserError:
            abort(409, message='A user with this username already exists')


class LoginApi(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True,
                            help='Your username')
        parser.add_argument('password', type=str, required=True,
                            help='Your password')
        args = parser.parse_args()

        token = login(args['username'], args['password'])

        if token is None:
            abort(403)

        return {
            'token': token
        }


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(request.headers, 'Authentication'):
            abort(403)

        auth_string = request.headers['Authentication']

        if not auth_string.lower().startswith('bearer '):
            abort(403)

        token = auth_string[7:]  # the bit after 'bearer '

        user = User.from_token(token)

        if user is None:
            abort(403)

        request.user = user

        return f(*args, **kwargs)
    return decorated_function
