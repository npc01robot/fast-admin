from flask import Blueprint
from flask_restful import Api

from apps.auth.views.auth import Login, RefreshToken, AsyncRoute, Sign
from apps.auth.views.wx_auth import WeChatRefreshToken, WeChatLogon

auth_api_bp = Blueprint('auth_api', __name__)
auth_api = Api(auth_api_bp)

auth_api.add_resource(Login, '/login')
auth_api.add_resource(RefreshToken, '/refreshToken')
auth_api.add_resource(AsyncRoute, '/asyncRoutes')
auth_api.add_resource(Sign, '/sign')
auth_api.add_resource(WeChatRefreshToken, '/wx_refreshToken')
auth_api.add_resource(WeChatLogon, '/wx_logon')
