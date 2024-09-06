import datetime
import time

from auth_ext.models import AuthExtUser, Department
from django.contrib.auth.hashers import check_password, make_password
from fast.settings import SIMPLE_JWT
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken


class AuthExtTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        """
        此方法往token的有效负载 payload 里面添加数据
        例如自定义了用户表结构，可以在这里面添加用户邮箱，头像图片地址，性别，年龄等可以公开的信息
        这部分放在token里面是可以被解析的，所以不要放比较私密的信息

        :param user: 用戶信息
        :return: token
        """
        token = super().get_token(user)
        # 添加个人信息
        token["name"] = user.username
        return token

    def validate(self, attrs):
        """
        此方法为响应数据结构处理
        原有的响应数据结构无法满足需求，在这里重写结构如下：
        {
            "refresh": "xxxx.xxxxx.xxxxx",
            "access": "xxxx.xxxx.xxxx",
            "expire": Token有效期截止时间,
        }
        """
        # data是个字典
        # 其结构为：{'refresh': '用于刷新token的令牌', 'access': '用于身份验证的Token值'}
        auth_user = AuthExtUser.objects.filter(username=attrs["username"]).first()
        if not auth_user:
            raise serializers.ValidationError("用户不存在！")
        if not check_password(attrs["password"], auth_user.password):
            raise serializers.ValidationError("密码错误！")
        data = super().validate(attrs)
        # 获取Token对象
        refresh = self.get_token(self.user)
        # 令牌到期时间
        current_time = datetime.datetime.now()
        # '指定有效期  业务token -- 1小时'
        expire_time = current_time + datetime.timedelta(
            seconds=SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].seconds
        )

        expire = expire_time.strftime("%Y/%m/%d %H:%M:%S")

        data["expires"] = expire  # 有效期
        # 用户名
        data["username"] = self.user.username
        data["roles"] = self.user.roles
        data["accessToken"] = data.pop("access")
        data["refreshToken"] = data.pop("refresh")

        return data


class AuthUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = AuthExtUser
        fields = "__all__"

    def save(self):
        if self.validated_data["username"] == "admin":
            self.validated_data["roles"] = ["admin", "common"]
            self.validated_data["permissions"] = [
                "permission:btn:add",
                "permission:btn:edit",
                "permission:btn:delete",
            ]
        else:
            self.validated_data["roles"] = ["common"]
            self.validated_data["permissions"] = [
                "permission:btn:add",
                "permission:btn:edit",
                "permission:btn:delete",
            ]
        self.validated_data["password"] = make_password(
            self.validated_data.pop("password")
        )
        user = super().save()
        return user


class AuthRefreshTokenSerializer(serializers.Serializer):
    refreshToken = serializers.CharField(required=True)
    token_class = RefreshToken

    def validate(self, attrs):
        refresh = self.token_class(attrs["refreshToken"])
        current_time = datetime.datetime.now()
        # '指定有效期  业务token -- 1小时'
        expire_time = current_time + datetime.timedelta(
            seconds=SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].seconds
        )
        expire = expire_time.strftime("%Y/%m/%d %H:%M:%S")
        data = {
            "accessToken": str(refresh.access_token),
            "refreshToken": str(refresh.token),
            "expires": expire,
        }

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()
        return data


class DepartmentSerializer(serializers.ModelSerializer):
    parent_id = serializers.SerializerMethodField()

    def get_parent_id(self, obj):
        if obj.parent:
            return obj.parent.id
        else:
            return None

    class Meta:
        model = Department
        fields = [
            "id",
            "name",
            "parent_id",
            "sort",
            "phone",
            "email",
            "type",
            "description",
            "remark",
            "status",
            "is_delete",
            "create_time",
            "update_time",
        ]
