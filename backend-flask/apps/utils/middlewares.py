import jwt
from flask import current_app, g, request


def verify_jwt(token, secret=None):
    """
    检验jwt
    :param token: jwt
    :param secret: 密钥
    :return: dict: payload
    """
    if not secret:
        secret = current_app.config["JWT_SECRET"]

    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
    except jwt.PyJWTError:
        payload = None

    return payload


"""用户认证机制==>每次请求前获取并校验token"""

"@app.before_request 不使@调用装饰器 在 init文件直接装饰"


def jwt_authentication():
    """
    1.获取请求头Authorization中的token
    2.判断是否以 Bearer开头
    3.使用jwt模块进行校验
    4.判断校验结果,成功就提取token中的载荷信息,赋值给g对象保存
    """
    auth = request.headers.get("Authorization")
    if auth and auth.startswith("Bearer "):
        "提取token 0-6 被Bearer和空格占用 取下标7以后的所有字符"
        token = auth[7:]
        "校验token"
        payload = verify_jwt(token)
        "判断token的校验结果"
        if payload:
            "获取载荷中的信息赋值给g对象"
            g.username = payload.get("username")
            g.refresh = payload.get("refresh")
