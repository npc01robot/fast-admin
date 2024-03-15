from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, Boolean, func, JSON, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash

from apps.models import db


class LogonUser(db.Model):
    """用户"""

    __tablename__ = 'logon_user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(150), unique=True, nullable=False)
    hash_password = Column(String(255), nullable=False, comment='密码')
    phone = Column(String(20), nullable=False, comment='手机号')
    email = Column(String(20), nullable=True, comment='邮箱')
    roles = Column(JSON, default=['common'], nullable=False,
                   comment='admin-管理员，common-普通用户')
    auths = Column(JSON, default=[], nullable=False, comment="""["btn_add", "btn_edit", "btn_delete"] 按钮权限""")
    create_at = Column(DateTime, default=datetime.now())
    update_at = Column(DateTime, default=datetime.now())
    login_date = Column(DateTime, default=datetime.now, comment="最后登陆时间", nullable=False,
                        onupdate=func.now())
    is_lock = Column(Boolean, default=False, nullable=False, comment='是否删除该用户')

    # 初始化
    def __init__(self, username, password, phone, email='', auths=[], roles=['common']):
        self.username = username
        self.password = password
        self.phone = phone
        self.email = email
        self.auths = auths
        self.roles = roles
        self.is_lock = False
        self.update()

    # 明文密码（只读）
    @property
    def password(self):
        raise AttributeError('不可读')

    # 写入密码，同时计算hash值，保存到模型中
    @password.setter
    def password(self, value):
        self.hash_password = generate_password_hash(value)

    '''------------------------------------------用户操作-----------------------------------------'''

    # 更新
    def update(self):
        self.update_at = datetime.now()
        db.session.add(self)
        db.session.commit()

    # 删除
    def delete(self):
        self.is_lock = True
        self.update()

    # 检查密码是否正确
    def check_password(self, password):
        return check_password_hash(self.hash_password, password)

    def update_login_date(self):
        self.login_date = datetime.now()
        self.update()


class LoginSessionCache(db.Model):
    __tablename__ = 'login_session_cache'

    id = Column(Integer, primary_key=True, autoincrement=True)
    openid = Column(String(255))  # openid
    session_key = Column(String(255))  # token
    update_at = Column(DateTime, default=datetime.now())

    # 定义对象
    def __init__(self, openid=None, session_key=None):
        self.openid = openid
        self.session_key = session_key
        self.update()  # 提交数据

    # 提交数据函数
    def update(self):
        self.update_at = datetime.now()
        db.session.add(self)
        db.session.commit()


class WechatUser(db.Model):
    __tablename__ = 'wechat_user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    openid = Column(String(255),nullable=False)  # openid
    username = Column(String(255),nullable=False)  # username
    phone = Column(String(255),nullable=False)
    email = Column(String(255),nullable=False)
    roles = Column(JSON, default=['common'], nullable=False,
                   comment='admin-管理员，common-普通用户')
    auths = Column(JSON, default=[], nullable=False, comment="""["btn_add", "btn_edit", "btn_delete"] 按钮权限""")
    create_at = Column(DateTime, default=datetime.now())
    update_at = Column(DateTime, default=datetime.now())
    is_lock = Column(Boolean, default=False)

    def __init__(self, openid=None, username=None,phone='', email='',
                 auths=[], roles=['common']):
        self.openid = openid
        self.username = username
        self.phone = phone
        self.email = email
        self.auths = auths
        self.roles = roles
        self.update()  # 提交数据

    def update(self,data={}):
        for key, value in data.items():
            if getattr(self,key):
                setattr(self, key, value)
        self.update_at = datetime.now()
        db.session.add(self)
        db.session.commit()
