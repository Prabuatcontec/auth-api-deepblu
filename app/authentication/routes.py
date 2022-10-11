from time import sleep
from flask import Blueprint, request, Response, session, Flask, jsonify, abort
from sqlalchemy import false
from flask_api import status
import bcrypt

blueprint = Blueprint(
    'authentication_blueprint',
    __name__,
    url_prefix=''
)

from app.authentication.models import Users 

        
@blueprint.route('/login_check', methods = ['POST'])
def authentication():
    username = request.form['_username'] 
    password = request.form['_password']
    validation = False
    if username is None or password is None:
        validation = True
    user = Users.query.filter_by(username = username).first()
    if user is None:
        validation = True
    if validation == False:
        token = Users().encode_auth_token(user.id, user.username, user.password, password, user.roles)
        if token == False:
            validation = True
        else: 
            return jsonify({ "token": token }), status.HTTP_200_OK
    if validation == True:
        return jsonify({ "code": status.HTTP_400_BAD_REQUEST, "message": "Bad credentials" }), status.HTTP_400_BAD_REQUEST
    

@blueprint.route('/decode')
def decode_token():
    user = Users().encode_auth_token(123, 'brian.crehan@azmoves.com')
    user = Users().decode_auth_token(user)
    responseBody = { "results": user }
    return jsonify(responseBody), status.HTTP_200_OK
