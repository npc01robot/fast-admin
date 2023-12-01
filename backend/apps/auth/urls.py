from flask import Blueprint
from flask_restful import Api

from apps.auth.views.auth import Login, RefreshToken, AsyncRoute

auth_api_bp = Blueprint('auth_api', __name__)
auth_api = Api(auth_api_bp)

auth_api.add_resource(Login, '/login')
auth_api.add_resource(RefreshToken, '/refreshToken')
auth_api.add_resource(AsyncRoute, '/asyncRoutes')
