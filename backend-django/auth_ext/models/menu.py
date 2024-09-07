from django.db import models, transaction


class Menu(models.Model):
    MENU_TYPE_CHOICES = (
        (0, "菜单"),
        (1, "iframe"),
        (2, "外链"),
        (3, "按钮"),
    )
    id = models.AutoField(primary_key=True)
    parent = models.ForeignKey(
        "self",
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="父菜单",
    )
    menu_type = models.IntegerField(choices=MENU_TYPE_CHOICES, default=0, verbose_name="菜单类型")
    title = models.CharField(max_length=200, null=True, blank=True, verbose_name="菜单名称")
    name = models.CharField(max_length=200, null=True, blank=True, verbose_name="路由名称")
    path = models.CharField(max_length=200, null=True, blank=True, verbose_name="路由路径")
    component = models.CharField(max_length=200, null=True, blank=True, verbose_name="组件路径")
    rank = models.IntegerField(null=True, blank=True, default=99, verbose_name="菜单排序")
    redirect = models.CharField(max_length=200, null=True, blank=True, verbose_name="重定向地址")
    icon = models.CharField(max_length=200, null=True, blank=True, verbose_name="图标")
    extra_icon = models.CharField(max_length=200, null=True, blank=True, verbose_name="额外图标")
    enter_transition = models.CharField(max_length=200, null=True, blank=True, verbose_name="进入动画")
    leave_transition = models.CharField(max_length=200, null=True, blank=True, verbose_name="离开动画")
    active_path = models.CharField(max_length=200, null=True, blank=True, verbose_name="激活路径")
    auths = models.CharField(max_length=200, null=True, blank=True, verbose_name="权限标识")
    frame_src = models.CharField(max_length=200, null=True, blank=True, verbose_name="iframe地址")
    frame_loading = models.CharField(max_length=200, null=True, blank=True)
    keep_alive = models.CharField(max_length=200, null=True, blank=True)
    hidden_tag = models.CharField(max_length=200, null=True, blank=True)
    fixed_tag = models.CharField(max_length=200, null=True, blank=True)
    show_link = models.CharField(max_length=200, null=True, blank=True)
    show_parent = models.CharField(max_length=200, null=True, blank=True)
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "auth_ext_menu"
        verbose_name = "菜单"
        verbose_name_plural = verbose_name

    def delete(self, using=None, keep_parents=False):
        with transaction.atomic(using=using):
            Menu.objects.filter(parent=self.id).update(is_deleted=True)
            self.is_deleted = True
            self.save()