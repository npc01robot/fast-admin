# DEBUG = True

# Flask Sqlalchemy Setting
DIALECT = "mysql"
DRIVER = "pymysql"
USERNAME = "root"
PASSWORD = "toor"
HOST = "127.0.0.1"
PORT = "3306"
DATABASE = "test"

# mysql 不会认识utf-8,而需要直接写成utf8
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(
    DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

SECRET_KEY = "xxxx"  # 实际开发请替换
JWT_SECRET = "xxxx"  # 实际开发请替换
JWT_REFRESH_DAYS = 7  # jwt refresh
JWT_EXPIRY_HOURS = 2  # jwt token
# Flask Bcrypt Setting
BCRYPT_LOG_ROUNDS = 1
