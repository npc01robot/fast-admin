"""
登录验证装饰器
python中的装饰器：会改变被装饰器装饰的函数的函数名(属性)
使用方法：放在method_decorators中
"""

import functools

from apps.auth.models.user import LoginSessionCache, WechatUser
from apps.utils.responser import Responser
from flask import g, request


def login_required(func):
    """让装饰器装饰的函数属性不会变 -- name属性"""

    # '第1种方法,使用functools模块的wraps装饰内部函数'
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not g.username:
            return {"message": "User must be authorized."}, 401
        elif not g.refresh:
            return {"message": "Do not use refresh token."}, 403
        else:
            return func(*args, **kwargs)

    # '第2种方法,在返回内部函数之前,先修改wrapper的name属性'
    # wrapper.__name__ = f.__name__
    return wrapper


def wechat_required(func=None):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if request.method == "POST":
            # 检验参数
            """获取openid和token 如果不存在返回None"""
            openid, session_key = request.json.get("openid"), request.json.get("token")
            """判断是否存在None的jsonkey"""
            if openid == None or session_key == None:
                return Responser.response_error("参数缺失", 400)

            """判断两个key的值是否为空"""
            if openid == "" or session_key == "":
                return Responser.response_error("参数缺失", 400)
            else:
                """获取openid 和 token 一致的记录"""
                if LoginSessionCache.query.filter_by(
                    openid=openid, session_key=session_key
                ).first():
                    """查询该用户的openid"""
                    if WechatUser.query.filter_by(openid=openid).first():
                        return func(*args, **kwargs)
                    else:
                        return Responser.response_error("未授权", 403)
                else:
                    return Responser.response_error("未登录", 401)
        else:
            """禁止get请求"""
            return Responser.response_error("请求方式不正确", 404)

    return wrapper
