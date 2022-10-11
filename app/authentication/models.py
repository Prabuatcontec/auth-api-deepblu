from app import db
from app import app
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
import datetime
import jwt
from jose import jws
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.backends import default_backend
from dotenv import load_dotenv
import bcrypt


class Users(db.Model):
    load_dotenv() 
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), unique=False)
    roles = db.Column(db.Text())

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = value # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)

    def encode_auth_token(self, user_id, username, password, _password, roles):
        """
        Generates the Auth Token
        :return: string
        """ 
        try:
            username = username
            _password = bytes(_password,'utf-8')
            password = bytes(password,'utf-8')

            if bcrypt.checkpw(_password, password):
                private_key_pem = str(app.config.get('JWT_PRIVATE_KEY'))
                with open(private_key_pem, "rb") as key_file:
                    pem_bytes = key_file.read()
                    passphrase = bytes(app.config.get('JWT_PASE_PHRASE'),'utf-8')
                    private_key = crypto_serialization.load_pem_private_key(pem_bytes, password=passphrase, backend=default_backend())

                payload = {
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7, seconds=300000),
                    'iat': datetime.datetime.utcnow(),
                    'username': username,
                    'id': user_id,
                    'roles': roles
                }
                return  jwt.encode(payload, private_key, algorithm='RS256')
            else:
                return False
            
        except Exception as e:
            return e

    def decode_auth_token(self, encoded):
        """
        Generates the Auth Token
        :return: string
        """ 
        try:
            public_key_pem = str(app.config.get('JWT_PUBLIC_KEY'))
            with open(public_key_pem, "rb") as key_file:
                public_key = key_file.read()
            
             
            return  jwt.decode(encoded, public_key, algorithms=["RS256"])
        except Exception as e:
            return e

    