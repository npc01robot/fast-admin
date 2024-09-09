from apps.auth.models.user import LogonUser
from flask_marshmallow.sqla import SQLAlchemySchema, auto_field
from marshmallow import (
    Schema,
    ValidationError,
    fields,
    post_load,
    validate,
    validates,
    validates_schema,
)

# post_dump([fn，pass_many，pass_original]) 注册要在序列化对象后调用的方法，它会在对象序列化后被调用。
# post_load([fn，pass_many，pass_original]) 注册反序列化对象后要调用的方法，它会在验证数据之后被调用。
# pre_dump([fn，pass_many]) 注册要在序列化对象之前调用的方法，它会在序列化对象之前被调用。
# pre_load([fn，pass_many]) 在反序列化对象之前，注册要调用的方法，它会在验证数据之前调用。


# 注册校验
class SignSchema(SQLAlchemySchema):
    id = auto_field(
        dump_only=True
    )  # read_only字段 表示id是只读字段，只允许从模型序列化
    username = fields.String(required=True)
    password = fields.String(required=True)
    phone = fields.String(
        required=True,
        validate=validate.Regexp("^1[3-9]\d{9}$", error="手机号码格式不正确"),
        error_messages={"Regexp": "手机格式不正确！"},
    )
    email = fields.Email()

    # 反序列化
    @post_load
    def create_user(self, data, **kwargs):
        return LogonUser(**data)

    @validates_schema
    def validate(self, data, **kwargs):
        username = data.get("username")
        user = LogonUser.query.filter_by(username=username).first()
        if user:
            # 如果包含phone字段，说明是注册，检查用户是否已存在
            raise ValidationError("注册失败,已存在该用户！")
        return data

    class Meta:
        model = LogonUser


# 用户操作schema
class UserSchema(SQLAlchemySchema):
    id = auto_field(
        dump_only=True
    )  # read_only字段 表示id是只读字段，只允许从模型序列化
    username = fields.String(required=True)
    password = fields.String(required=True)

    # 反序列化
    @post_load
    def update_login_time(self, data, **kwargs):
        user = LogonUser.query.filter_by(username=data.get("username")).first()
        user.update_login_date()
        return user

    @validates_schema
    def validate(self, data, **kwargs):
        username = data.get("username")
        user = LogonUser.query.filter_by(username=username).first()
        if not user:
            # 如果包含phone字段，说明是注册，检查用户是否已存在
            raise ValidationError(message="用户名不存在！", field_name="username")
        else:
            if user.check_password(data["password"]):
                return data
            else:
                raise ValidationError(message="密码验证失败！", field_name="password")

    class Meta:
        model = LogonUser
