from flask_marshmallow.sqla import SQLAlchemySchema, auto_field
from marshmallow import fields, Schema, post_load, validate, validates, validates_schema

from apps.auth.models.user import LogonUser


# post_dump([fn，pass_many，pass_original]) 注册要在序列化对象后调用的方法，它会在对象序列化后被调用。
# post_load([fn，pass_many，pass_original]) 注册反序列化对象后要调用的方法，它会在验证数据之后被调用。
# pre_dump([fn，pass_many]) 注册要在序列化对象之前调用的方法，它会在序列化对象之前被调用。
# pre_load([fn，pass_many]) 在反序列化对象之前，注册要调用的方法，它会在验证数据之前调用。

# 用户校验
class UserSchema(SQLAlchemySchema):
    id = auto_field(dump_only=True)  # read_only字段 表示id是只读字段，只允许从模型序列化
    username = fields.String(required=True)
    password = fields.String(required=True)
    phone = fields.String(validate=validate.Regexp("^1[3-9]\d{9}$", error="手机号码格式不正确"),
                          error_messages={"Regexp": "手机格式不正确"})

    # 反序列化
    @post_load
    def create_user(self, data, **kwargs):
        return LogonUser(**data)

    @validates_schema
    def validate(self, data, **kwargs):
        username = data.get('username')
        user = LogonUser.query.filter_by(username=username).first()
        if 'phone' in data and user:
            # 如果包含phone字段，说明是注册，检查用户是否已存在
            raise Exception({"对不起,已存在该用户！"})
        elif 'phone' in data and not user:
            return data  # 可以继续注册流程
        elif 'password' in data and user:
            # 如果包含password字段，说明是登录，验证用户名和密码
            if user.check_password(data['password']):
                return data
            else:
                raise Exception({"对不起,密码输入错误！"})
        else:
            raise Exception({"对不起,没有该用户！"})

    class Meta:
        model = LogonUser
