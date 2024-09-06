from auth_ext.models.role import Role
from django.contrib.auth.models import AbstractUser, Permission
from django.db import models


class AuthExtUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True, verbose_name="用户名")
    password = models.CharField(max_length=255, null=False, verbose_name="密码")
    nickname = models.CharField(max_length=150, null=False, verbose_name="昵称")
    avatar = models.CharField(max_length=255, null=True, verbose_name="头像")
    roles = models.ManyToManyField(
        Role,
        related_name="role",
        through_fields=("user", "role"),
    )
    permissions = models.ManyToManyField(
        Permission,
        related_name="permission",
        through_fields=("user", "permission"),
    )
    phone = models.CharField(max_length=11, verbose_name="手机号")
    email = models.EmailField(max_length=20, verbose_name="邮箱")
    description = models.CharField(max_length=2000, null=True, verbose_name="描述")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_delete = models.BooleanField(default=False, verbose_name="是否移除")

    class Meta(object):
        db_table = "auth_ext_user"
        verbose_name = "用户表"
        managed = True


class LoginLog(models.Model):
    user = models.ForeignKey(AuthExtUser, on_delete=models.CASCADE)
    ip = models.CharField(max_length=20, verbose_name="IP地址")
    address = models.CharField(max_length=100, verbose_name="地址")
    system = models.CharField(max_length=50, verbose_name="系统")
    browser = models.CharField(max_length=50, verbose_name="浏览器")
    summary = models.CharField(max_length=200, verbose_name="描述")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="登录时间")
    operating_time = models.IntegerField(default=0, verbose_name="使用时长(分钟)")

    class Meta(object):
        db_table = "login_log"
        verbose_name = "登录日志"
        managed = True

    @classmethod
    def op_log(cls, request, summary):
        if request.META.has_key("HTTP_X_FORWARDED_FOR"):
            ip = request.META["HTTP_X_FORWARDED_FOR"]
        else:
            ip = request.META["REMOTE_ADDR"]
        address = request.META.get("HTTP_X_REAL_IP", "")
        system = request.META.get("HTTP_USER_AGENT", "")
        browser = request.META.get("HTTP_USER_AGENT", "")
        cls.objects.create(
            ip=ip, address=address, system=system, browser=browser, summary=summary
        )
