from flask_cors import CORS

from flask import Flask  # flask
from flask_migrate import Migrate

from apps.models import db
from config.routes import register_routes
from apps.utils.middlewares import jwt_authentication
from config import config

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
# 需要将每个app下面的models在这个地方引用一下

migrate = Migrate(app, db)
