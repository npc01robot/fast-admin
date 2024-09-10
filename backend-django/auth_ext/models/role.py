from auth_ext.models.menu import Menu
from django.db import models


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=50, null=False, blank=False, unique=True, verbose_name="角色名称"
    )
    code = models.CharField(
        max_length=50, null=False, blank=False, unique=True, verbose_name="角色code"
    )
    status = models.BooleanField(default=True, verbose_name="状态")
    remark = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="备注"
    )
    menu = models.ManyToManyField(
        Menu,
        through="RoleMenu",
        through_fields=("role", "menu"),
        verbose_name="菜单",
    )

    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "auth_ext_role"
        verbose_name = "角色"
        managed = True

    def delete(self, using=None, keep_parents=False):
        if self.code == "admin":
            raise Exception("不能删除admin角色!")
        self.is_deleted = True
        self.save()


class RoleMenu(models.Model):
    id = models.AutoField(primary_key=True)
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, related_name="role_menu", verbose_name="角色"
    )
    menu = models.ForeignKey(
        Menu, on_delete=models.CASCADE, related_name="role_menu", verbose_name="菜单"
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "auth_ext_role_menu"
        verbose_name = "角色菜单"
        managed = True
