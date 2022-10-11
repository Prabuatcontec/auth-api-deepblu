from flask import request
from flask_restplus import Resource, fields, Namespace

from app.models.users import UsersModel
from app.schemas.users import UsersSchema

USER_NOT_FOUND = "User not found."
USER_ALREADY_EXISTS = "User '{}' Already exists."

user_ns = Namespace('user', description='User related operations')
users_ns = Namespace('users', description='Users related operations')

user_schema = UsersSchema()
users_list_schema = UsersSchema(many=True)

# Model required by flask_restplus for expect
user = users_ns.model('Users', {
    'username': fields.String('Username of Login')
})


class User(Resource):
    def get(self, id):
        user_data = UsersModel.find_by_id(id)
        if user_data:
            return user_schema.dump(user_data)
        return {'message': USER_NOT_FOUND}, 404

    def delete(self, id):
        user_data = UsersModel.find_by_id(id)
        if user_data:
            user_data.delete_from_db()
            return {'message': "Users Deleted successfully"}, 200
        return {'message': USER_NOT_FOUND}, 404


class UsersList(Resource):
    @users_ns.doc('Get all the Users')
    def get(self):
        return users_list_schema.dump(UsersModel.find_all()), 200

    @users_ns.expect(user)
    @users_ns.doc('Create a User')
    def post(self):
        user_json = request.get_json()
        name = user_json['username']
        if UsersModel.find_by_name(name):
            return {'message': USER_ALREADY_EXISTS.format(name)}, 400

        user_data = user_schema.load(user_json)
        user_data.save_to_db()

        return user_schema.dump(user_data), 201
