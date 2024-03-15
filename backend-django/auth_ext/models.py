from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class AuthExtUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=255, null=False, verbose_name='密码')
    phone = models.CharField(max_length=11, verbose_name='手机号')
    email = models.EmailField(max_length=20, verbose_name='邮箱')
    roles = models.JSONField(default=['common'], null=False, verbose_name='admin-管理员，common-普通用户')
    auths = models.JSONField(default=list, null=False, verbose_name='["btn_add", "btn_edit", "btn_delete"] 按钮权限')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否移除')

    class Meta(object):
        db_table = 'auth_ext_user'
        verbose_name = '用户表'
        managed = True


