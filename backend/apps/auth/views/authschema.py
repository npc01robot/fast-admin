from marshmallow import fields, Schema


# 用户校验
class UserSchema(Schema):
    username = fields.String()
    password = fields.String()

    class Meta:
        fields = ["username", "password"]
