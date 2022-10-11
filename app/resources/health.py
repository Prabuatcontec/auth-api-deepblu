
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from flask_restplus import Resource, Namespace


health_ns = Namespace('health', description='Health check' )



class Health(Resource):
    @health_ns.doc('Get Container health', security = 'apiKey')
    def get(self):
        return {'status': 'up'}, 200