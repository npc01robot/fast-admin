from io import BytesIO

from django.db import models, transaction

from generics.models import ImportExportRecord
from generics.tasks import upload_handler
import pandas as pd


class Basic(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=100, null=False, verbose_name="名称")
    parent = models.ForeignKey(
        "self",
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="上级",
    )
    sort = models.IntegerField(default=0, verbose_name="排序")

    remark = models.CharField(
        max_length=2000, null=True, blank=True, verbose_name="备注"
    )
    GUARANTEE = 1  # 担保单位
    GUARANTEE_TYPE = 2  # 担保类型
    FINANCE = 3  # 金融机构
    LOAN_UNIT = 4  # 贷款单位
    LOAN_TYPE = 5  # 贷款类型

    TYPE_CHOICES = (
        (GUARANTEE, "担保单位"),
        (GUARANTEE_TYPE, "担保类型"),
        (FINANCE, "金融机构"),
        (LOAN_UNIT, "贷款单位"),
        (LOAN_TYPE, "贷款类型"),
    )
    type = models.IntegerField(choices=TYPE_CHOICES, default=1, verbose_name="类型")
    creator = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="创建人"
    )
    status = models.BooleanField(default=True, verbose_name="状态 0-禁用 1-启用")
    is_deleted = models.BooleanField(default=False, verbose_name="是否移除")

    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta(object):
        db_table = "basic"
        verbose_name = "基础信息"
        managed = True

    def delete(self, using=None, keep_parents=False):
        with transaction.atomic(using=using):
            self.is_deleted = True
            children = Basic.objects.filter(parent=self)
            update_basic = []
            for child in children:
                child.is_deleted = False
                update_basic.append(child)
            Basic.objects.bulk_update(update_basic, ["is_deleted"])
            self.save()
