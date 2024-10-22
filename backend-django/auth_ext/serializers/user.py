import datetime

from auth_ext.models.department import Department
from auth_ext.models.role import Role
from auth_ext.models.user import AuthExtUser
from django.contrib.auth.hashers import check_password, make_password
from fast.settings import SIMPLE_JWT, BASE_URL
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from utils.storage import file_system_storage


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
        roles = self.user.roles.values_list("code", flat=True)
        data["roles"] = roles
        data["accessToken"] = data.pop("access")
        data["refreshToken"] = data.pop("refresh")

        return data


class AuthUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True)
    roles = serializers.ListField(read_only=True)
    permissions = serializers.ListField(read_only=True)
    avatar = serializers.SerializerMethodField()

    def get_avatar(self, obj):
        if obj.avatar:
            return BASE_URL + file_system_storage.url(obj.avatar)
        return ""

    class Meta:
        model = AuthExtUser
        fields = "__all__"

    def save(self):
        if self.validated_data["username"] == "admin":
            # 初始化权限
            admin = Role.objects.filter(code="admin").first()
            if not admin:
                admin = Role.objects.create(code="admin", name="管理员", remark="admin")
            common = Role.objects.filter(code="common").first()
            if not common:
                common = Role.objects.create(
                    code="common", name="普通用户", remark="common"
                )

            self.validated_data["roles"] = [admin, common]
            self.validated_data["permissions"] = [
                "permission:btn:add",
                "permission:btn:edit",
                "permission:btn:delete",
            ]
        else:
            self.validated_data["roles"] = [Role.objects.filter(code="common").first()]
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


class AuthUserInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField()
    nickname = serializers.CharField()
    avatar = serializers.SerializerMethodField()
    phone = serializers.CharField()
    email = serializers.EmailField()
    gender = serializers.CharField(default=0)
    dept = serializers.SerializerMethodField()
    depart_id = serializers.IntegerField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)
    status = serializers.BooleanField()
    description = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    remark = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    def get_dept(self, obj):
        if obj.dept:
            return {"id": obj.dept.id, "name": obj.dept.name}
        return {}

    def get_avatar(self, obj):
        if obj.avatar:
            return BASE_URL + file_system_storage.url(obj.avatar)
        return ""

    def validate(self, attrs):
        depart_id = attrs.pop("depart_id", None)
        if depart_id:
            dept = Department.objects.filter(id=depart_id).first()
            attrs["dept"] = dept
        return attrs

    def create(self, validated_data):
        self.validated_data["password"] = make_password(
            self.validated_data.pop("password")
        )
        user = AuthExtUser.objects.create(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.nickname = validated_data.get("nickname", instance.nickname)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.email = validated_data.get("email", instance.email)
        instance.gender = validated_data.get("gender", instance.gender)
        instance.dept = validated_data.get("dept", instance.dept)
        instance.status = validated_data.get("status", instance.status)
        instance.description = validated_data.get("description", instance.description)
        instance.remark = validated_data.get("remark", instance.remark)
        instance.save()
        return instance

    class Meta:
        model = AuthExtUser
        fields = "__all__"


class AuthUserPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        password = self.initial_data.pop("password", None)
        if not password:
            raise serializers.ValidationError("密码不能为空！")
        self.initial_data["password"] = make_password(password)
        return attrs

    def update(self, instance, validated_data):
        instance.password = validated_data.get("password", instance.password)
        instance.save()
        return instance

    class Meta:
        model = AuthExtUser
        fields = ["password"]
