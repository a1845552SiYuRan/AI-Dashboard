from flask_restx import Namespace, Resource, fields, abort
from flask import request
from util.helper import *
from util.models import *

api = Namespace('auth', description='Authentication Services')

@api.route('/login')
class Login(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Missing Username/Password')
    @api.response(403, 'Invalid Username/Password')
    @api.expect(login_details(api))
    @api.doc(description='''
        This is used to authenticate a verified account created through signup.
        Returns a auth token which should be passed in subsequent calls to the api
        to verify the user.
    ''')
    def post(self):
        if not request.json:
            abort(400, 'Malformed Request')
        (username, password) = unpack(request.json, 'username', 'password')
        if (password != "admin"):
            abort(403,'Invalid Username/Password')
        t = gen_token()
        return {
            'token': t,
        }
