import math

from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from apps.auth.models.user import LoginSessionCache, WechatUser
from apps.auth.views.wx_auth_schema import WeChatSignSchema
from apps.utils.responser import Responser
from apps.utils.status import HTTP_400_BAD_REQUEST
from sdk.wechat import WXSDK_jscode2session


class WeChatRefreshToken(Resource):
    """
    微信 刷新 token 机制 后期需优化
    """
    def post(self):
        params = request.json
        code = params.get('code')
        if code is None:
            return Responser.response_error(msg='code fileds Missing')
        else:
            try:
                '''获取用户的openid 和 session_key'''
                # 获取用户openid和session_key
                # wechet_data = WXSDK_jscode2session(request.json['code'])
                # openid, session_key = wechet_data['openid'], wechet_data['session_key']
                # 获取用户信息
                openid, session_key = "testopenid","session_test_token"
                '''登录逻辑(更新和新建)'''
                log = LoginSessionCache.query.filter_by(openid=openid).first()
                if log:
                    '''存在就更新session_key'''
                    '''更新用户数据'''
                    log.session_key = session_key
                    log.update()
                else:
                    '''不存在就创建登录记录写入id和sessionkey'''
                    LoginSessionCache(openid, session_key)
                    res = {
                        "openid":openid,
                        "token":session_key
                    }
                    return Responser.response_success(data=res)
            except Exception as e:
                return Responser.response_error(msg=e)


class WeChatLogon(Resource):
    """
    用于首次注册,获取用户信息，返回uerid等操作
    """
    schema = WeChatSignSchema()

    def post(self):
        params = request.json
        try:
            params = self.schema.load(params)
            user = self.schema.create_info(params)
            res = self.schema.dump(user)
            return Responser.response_success(data=res)
        except ValidationError as err:
            return Responser.response_error(msg=err.messages, code=HTTP_400_BAD_REQUEST)

    def get(self):
        params = request.args
        try:
            user = self.schema.get_info(params)
            res = self.schema.dump(user)
            return Responser.response_success(data=res)
        except ValidationError as err:
            return Responser.response_error(msg=err.messages, code=HTTP_400_BAD_REQUEST)
