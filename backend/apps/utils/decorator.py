"""
登录验证装饰器
python中的装饰器：会改变被装饰器装饰的函数的函数名(属性)
使用方法：放在method_decorators中
"""
import functools

from flask import g

def login_required(func):
    '让装饰器装饰的函数属性不会变 -- name属性'
    # '第1种方法,使用functools模块的wraps装饰内部函数'
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not g.username:
            return {'message': 'User must be authorized.'}, 401
        elif not g.refresh:
            return {'message': 'Do not use refresh token.'}, 403
        else:
            return func(*args, **kwargs)
    # '第2种方法,在返回内部函数之前,先修改wrapper的name属性'
    # wrapper.__name__ = f.__name__
    return wrapper
