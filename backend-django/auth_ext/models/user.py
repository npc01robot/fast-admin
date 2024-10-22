from auth_ext.models.department import Department
from auth_ext.models.permission import Permission
from auth_ext.models.role import Role
from django.contrib.auth.models import AbstractUser
from django.db import models, transaction


class AuthExtUser(AbstractUser, models.Model):
    username = models.CharField(max_length=150, unique=True, verbose_name="用户名")
    password = models.CharField(max_length=255, null=False, verbose_name="密码")
    nickname = models.CharField(max_length=150, null=False, verbose_name="昵称")
    avatar = models.CharField(
        max_length=255, null=True, blank=True, default=None, verbose_name="头像"
    )
    roles = models.ManyToManyField(
        Role, related_name="users", through="UserRoles", verbose_name="角色"
    )
    permissions = models.JSONField(
        null=True, blank=True, default=None, verbose_name="权限"
    )
    dept = models.ForeignKey(
        Department,
        related_name="users",
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
        verbose_name="部门",
    )
    phone = models.CharField(max_length=11, verbose_name="手机号")
    email = models.EmailField(max_length=20, verbose_name="邮箱")
    description = models.CharField(max_length=2000, null=True, verbose_name="描述")
    remark = models.CharField(
        max_length=2000, null=True, blank=True, default=None, verbose_name="备注"
    )
    gender = models.IntegerField(default=0, verbose_name="性别,0-未知,1-男,2-女")
    status = models.BooleanField(default=True, verbose_name="状态")
    is_deleted = models.BooleanField(default=False, verbose_name="是否移除")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta(object):
        db_table = "auth_ext_user"
        verbose_name = "用户表"
        managed = True

    def delete(self, using=None, keep_parents=False):
        if self.username == "admin":
            raise Exception("不能删除admin用户")
        with transaction.atomic(using=using):
            self.is_deleted = True
            self.save()


class UserRoles(models.Model):
    user = models.ForeignKey(AuthExtUser, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_deleted = models.BooleanField(default=False, verbose_name="是否移除")

    class Meta(object):
        db_table = "auth_ext_user_roles"
        verbose_name = "用户角色关系表"
        managed = True


class UserPermissions(models.Model):
    user = models.ForeignKey(AuthExtUser, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_deleted = models.BooleanField(default=False, verbose_name="是否移除")

    class Meta(object):
        db_table = "auth_ext_user_permissions"
        verbose_name = "用户权限关系表"
        managed = True
