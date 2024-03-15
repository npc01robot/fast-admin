from datetime import timedelta, datetime

import jwt
from flask import current_app


def generate_tokens(username, need_refresh_token=True):
    """
    生成token 和refresh_token
    :param username: 用户id
    :param need_refresh_token 是否需要刷新
    :return: token2小时, refresh_token14天
    """
    # pass
    # '生成时间信息'
    current_time = datetime.utcnow()
    # '指定有效期  业务token -- 2小时'
    expire_time = current_time + timedelta(hours=current_app.config['JWT_EXPIRY_HOURS'] + 8)

    expire = expire_time.strftime('%Y/%m/%d %H:%M:%S')
    # '生成业务token  refresh 标识是否是刷新token''
    token = generate_jwt({'username': username, 'refresh': False}, expiry=expire_time)

    # '给刷新token设置一个默认值None'
    refresh_token = None
    # '根据传入的参数判断是否需要生成刷新token''
    # '不需要生成的传入need_refresh_token=False,需要的传入True或不传使用默认值'
    if need_refresh_token:
        '指定有效期  刷新token -- 14天'
        refresh_expires = current_time + timedelta(days=current_app.config['JWT_REFRESH_DAYS'])

        '生成刷新token'
        refresh_token = generate_jwt({'username': username, 'refresh': True}, expiry=refresh_expires)
    # '返回这两个token''
    return token, refresh_token, expire


def generate_jwt(payload, expiry, secret=None):
    """
    生成jwt
    :param payload: dict 载荷
    :param expiry: datetime 有效期
    :param secret: 密钥
    :return: jwt
    """
    _payload = {'exp': expiry}
    _payload.update(payload)

    if not secret:
        secret = current_app.config['JWT_SECRET']

    token = jwt.encode(_payload, secret, algorithm='HS256')
    return token
