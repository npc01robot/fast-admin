from apps.auth.urls import auth_api_bp
from apps.test.urls import item_api_bp
# 路由配置
def register_routes(app):
    app.register_blueprint(item_api_bp, url_prefix='/item')
    app.register_blueprint(auth_api_bp, url_prefix='/auth')
