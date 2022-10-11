from flask import session
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from flask_restplus import Resource, fields, Namespace
import datetime
import jwt
from flask_api import status
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.backends import default_backend
from dotenv import load_dotenv
import bcrypt
from functools import wraps
from app.models.users import UsersModel
from app.schemas.users import UsersSchema
import os
from app.helper.auth_middleware import Token
from app.helper.decorator import decorator
USER_NOT_FOUND = "User not found."
USER_ALREADY_EXISTS = "User '{}' Already exists."

autho_ns = Namespace('authorization', description='authorization',  security='apiKey', decorators= [Token().token_required])

user_schema = UsersSchema()
users_list_schema = UsersSchema(many=True)

# Model required by flask_restplus for expect
user = autho_ns.model('Authorization', {
    '_username': fields.String('Username'),
    '_password': fields.String('Password')
})


class Authorization(Resource):
    @autho_ns.doc('Get User Detail', security = 'apiKey')
    @decorator(permission='USER,BRANCH_ADMIN,COMPANY_ADMIN')
    def get(self, id):
        item_data = UsersModel.find_by_id(session['id'])
        if item_data:
            return user_schema.dump(item_data)
        return {'message': id}, 404