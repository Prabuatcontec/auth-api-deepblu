import imp
from app.resources.authorization import Authorization, autho_ns
from flask import Flask, Blueprint, jsonify
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from flask_restplus import Api
from app.ma import ma
from app.db import db
from app.resources.users import User, UsersList, users_ns, user_ns
from app.resources.authentication import Authentication, auth_ns
from app.resources.health import Health, health_ns
from marshmallow import ValidationError
from app.config import config_dict
from decouple import config

# # WARNING: Don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

app_config = config_dict[get_config_mode.capitalize()]



app = Flask(__name__)
app.config['SECRET_KEY'] = config('SECRET_KEY', default=None)
app.config['JWT_PRIVATE_KEY'] = config('JWT_PRIVATE_KEY', default=None)
app.config['JWT_PUBLIC_KEY'] = config('JWT_PUBLIC_KEY', default=None)
app.config['JWT_PASE_PHRASE'] = config('JWT_PASE_PHRASE', default=None)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config.from_object(app_config)
bluePrint = Blueprint('api', __name__, url_prefix='/api')
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token"
    }
}

api = Api(bluePrint, doc='/doc', title='eEndorsement Auth API', authorizations=authorizations)
app.register_blueprint(bluePrint)


api.add_namespace(user_ns)
api.add_namespace(users_ns)
api.add_namespace(auth_ns)
api.add_namespace(autho_ns)
api.add_namespace(health_ns)




@app.before_first_request
def create_tables():
    db.create_all()


@api.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400


user_ns.add_resource(User, '/<int:id>')
users_ns.add_resource(UsersList, "")
auth_ns.add_resource(Authentication, "")
autho_ns.add_resource(Authorization, "")
health_ns.add_resource(Health, "")
db.init_app(app)
ma.init_app(app)