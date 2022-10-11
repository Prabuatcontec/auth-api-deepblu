from flask import request
from flask_restplus import Resource, fields, Namespace
import datetime
import jwt
from flask_api import status
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.backends import default_backend
import bcrypt
from app.models.users import UsersModel
from app.schemas.users import UsersSchema
import os
USER_NOT_FOUND = "User not found."
USER_ALREADY_EXISTS = "User '{}' Already exists."

auth_ns = Namespace('authentication', description='Athentication')

user_schema = UsersSchema()
users_list_schema = UsersSchema(many=True)

# Model required by flask_restplus for expect
user = auth_ns.model('Authentication', {
    '_username': fields.String('Username'),
    '_password': fields.String('Password')
})


class Authentication(Resource):
    @auth_ns.expect(user)
    @auth_ns.doc('Authenticate User')
    def post(self):
        _username = request.form.get('_username')
        _password = request.form.get('_password')

        validation = False
        if _username is None or _password is None:
            validation = True
        users = UsersModel.find_by_name(_username) 

        if users:            
            try:
                username = bytes(users.username,'utf-8')
                password = bytes(users.password,'utf-8')
                _password = bytes(_password,'utf-8')
                user_id = users.id 
                roles = users.roles
                
                
                if bcrypt.checkpw(_password, password):
                    private_key_pem = str(os.getenv('JWT_PRIVATE_KEY'))
                    with open(private_key_pem, "rb") as key_file:
                        pem_bytes = key_file.read()
                        passphrase = bytes(os.getenv('JWT_PASE_PHRASE'),'utf-8')
                        private_key = crypto_serialization.load_pem_private_key(pem_bytes, password=passphrase, backend=default_backend())

                    token =  jwt.encode(users.json(), private_key, algorithm='RS256')
                    return { "token": token }, status.HTTP_200_OK
                else:
                   validation = True
                
            except Exception as e:
                return e
        else: 
            validation = True
        if validation == True:
            return { "code": status.HTTP_400_BAD_REQUEST, "message": "Bad credentials" }, status.HTTP_400_BAD_REQUEST