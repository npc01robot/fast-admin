from marshmallow import fields, validate, post_dump, pre_dump, ValidationError
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from apps.auth.models.user import WechatUser


class WeChatSignSchema(SQLAlchemySchema):
    id = auto_field(dump_only=True)  # read_only字段 表示id是只读字段，只允许从模型序列化
    openid = fields.String(required=True)
    username = fields.String(required=True)
    email = fields.Email()
    phone = fields.String(required=True, validate=validate.Regexp("^1[3-9]\d{9}$", error="手机号码格式不正确"),
                          error_messages={"Regexp": "手机格式不正确！"})

    def get_info(self,data,**kwargs):
        userid = data.get("id")
        user = WechatUser.query.filter_by(id=userid).first()
        return user

    def create_info(self,data,**kwargs):
        openid = data.get("openid")
        if openid:
            user = WechatUser.query.filter_by(openid=openid).first()
            if user:
                user.update(data)
            else:
                user = WechatUser(**data)
            return user
        raise ValidationError("注册失败,未授权！")

    class Meta:
        model = WechatUser
