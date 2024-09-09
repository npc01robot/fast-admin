from apps.models import db
from apps.utils.middlewares import jwt_authentication
from config import config
from config.routes import register_routes
from flask import Flask  # flask
from flask_cors import CORS
from flask_migrate import Migrate

app = Flask(__name__)

CORS(app)
# 引入全局配置
app.config.from_object(config)

# "添加请求钩子"
app.before_request(jwt_authentication)

# url
register_routes(app)
# 数据库迁移相关
db.init_app(app)
migrate = Migrate(app, db)
