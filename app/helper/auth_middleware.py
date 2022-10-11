from functools import wraps
import jwt
from flask import request, abort, session, jsonify
import os
from app.models.users import UsersModel 

class Token():
    def token_required(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            # jwt is passed in the request header
            if 'Authorization' in request.headers:
                token = request.headers['Authorization']
            # return 401 if token is not passed  
            if not token:
                return jsonify({'message' : 'Token is missing !!'}), 401
    
            try:
                public_key_pem = str(os.getenv('JWT_PUBLIC_KEY'))
                with open(public_key_pem, "rb") as key_file:
                    public_key = key_file.read()
                # decoding the payload to fetch the stored details
                token = token.replace("Bearer ","")

                data = jwt.decode(token, public_key, algorithms=["RS256"]) 
                
                current_user = UsersModel.find_by_id(data['id'])
                session['id'] = data['id']

            except:
                return jsonify({
                    'message' : 'Token is invalid !!'
                }), 401
            # returns the current logged in users contex to the routes
            return  f(current_user, *args, **kwargs)
    
        return decorated