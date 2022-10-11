from flask import  request, jsonify
import os
import jwt
class decorator:
    def __init__(self, permission='b'):
        self.permission = permission

    def __call__(self, func):
        def my_logic(*args, **kwargs):
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
                
                rules = self.permission.split(",")
                roles = data['roles'].replace("ROLE_","").split(",") 
                for i in rules:
                   if i in roles:
                         result = func(*args, **kwargs)
                         return result
                return {
                    'message' : 'No Permission'
                }, 401
            except: 
                return jsonify({
                    'message' : 'Token is invalids !!'
                }), 401
            

        return my_logic