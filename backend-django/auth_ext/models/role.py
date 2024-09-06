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
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "role"
        verbose_name = "角色"
        managed = True
