from django.db import models, transaction


class Department(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=100, null=False, verbose_name="部门名称")
    parent = models.ForeignKey(
        "self",
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="上级部门",
    )
    sort = models.IntegerField(default=0, verbose_name="排序")
    phone = models.CharField(max_length=11, null=True, blank=True, verbose_name="电话")
    email = models.EmailField(
        max_length=20, null=True, blank=True, verbose_name="Email"
    )

    COMPANY = "1"
    FILIABLE = "2"
    DEPT = "3"
    TYPE_CHOICES = (
        (COMPANY, "总公司"),
        (FILIABLE, "分公司"),
        (DEPT, "部门"),
    )
    type = models.CharField(
        max_length=2,
        default="1",
        choices=TYPE_CHOICES,
        db_index=True,
        verbose_name="类型",
    )

    description = models.CharField(max_length=2000, null=True, verbose_name="描述")
    remark = models.CharField(
        max_length=2000, null=True, blank=True, verbose_name="备注"
    )
    status = models.BooleanField(default=True, verbose_name="状态 0-禁用 1-启用")
    is_deleted = models.BooleanField(default=False, verbose_name="是否移除")

    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta(object):
        db_table = "auth_ext_department"
        verbose_name = "部门表"
        managed = True

    def delete(self, using=None, keep_parents=False):
        with transaction.atomic(using=using):
            self.is_deleted = True
            self.save()
