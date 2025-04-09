import io

import pandas as pd
from django.core.paginator import Paginator
from django.db import models, transaction

from auth_ext.models import AuthExtUser


class Credit(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        default="",
        unique=True,
        verbose_name="授信编号",
    )
    name = models.CharField(
        max_length=200, null=False, blank=False, verbose_name="授信名称"
    )
    organization = models.CharField(
        max_length=200, null=False, blank=False, verbose_name="授信机构"
    )
    amount = models.DecimalField(
        max_digits=15, decimal_places=2, verbose_name="授信金额"
    )
    surplus_amount = models.DecimalField(
        max_digits=15, decimal_places=2, verbose_name="剩余金额"
    )
    "集团董事会"
    group_chairman = models.BooleanField(
        default=False, verbose_name="集团董事会"
    )
    "集团党委会"
    group_deputy_chairman = models.BooleanField(
        default=False, verbose_name="集团党委会"
    )
    "子公司董事会"
    sub_chairman = models.BooleanField(
        default=False, verbose_name="子公司董事会"
    )
    "子公司党委会"
    sub_deputy_chairman = models.BooleanField(
        default=False, verbose_name="子公司党委会"
    )
    start_date = models.DateField(verbose_name="起始日期")
    end_date = models.DateField(verbose_name="终止日期")
    remark = models.TextField(null=True, blank=True, verbose_name="备注")

    "三级公司党委会日期"
    three_deputy_chairman_date = models.DateField(
        null=True, blank=True, verbose_name="三级公司党委会日期"
    )
    "三级公司董事会日期"
    three_chairman_date = models.DateField(
        null=True, blank=True, verbose_name="三级公司董事会日期"
    )
    "二级公司党委会日期"
    two_deputy_chairman_date = models.DateField(
        null=True, blank=True, verbose_name="二级公司党委会日期"
    )
    "二级公司董事会日期"
    two_chairman_date = models.DateField(
        null=True, blank=True, verbose_name="二级公司董事会日期"
    )
    "集团党委会日期"
    group_deputy_chairman_date = models.DateField(
        null=True, blank=True, verbose_name="集团党委会日期"
    )
    "集团董事会日期"
    group_chairman_date = models.DateField(
        null=True, blank=True, verbose_name="集团董事会日期"
    )
    "三级董事会决议"
    three_chairman_decision_file = models.CharField(
        max_length=500, null=True, blank=True, verbose_name="三级董事会决议"
    )
    "二级董事会决议"
    two_chairman_decision_file = models.CharField(
        max_length=500, null=True, blank=True, verbose_name="二级董事会决议"
    )
    "集团董事会决议"
    group_chairman_decision_file = models.CharField(
        max_length=500, null=True, blank=True, verbose_name="集团董事会决议"
    )
    create_user = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="创建人"
    )
    dept = models.IntegerField(null=True, blank=True, verbose_name="部门")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "credit"
        managed = True
        verbose_name = "授信信息"
        verbose_name_plural = verbose_name

    def delete(self, using=None, keep_parents=False):
        with transaction.atomic(using=using):
            self.is_deleted = True
            self.save()

    @classmethod
    def export_data(
        cls, page=1, page_size=30, filter_dict={}, export_all=False, **kwargs
    ):
        queryset = cls.objects.filter(is_deleted=False, **filter_dict)
        ids = kwargs.get("ids")
        if ids:
            queryset = queryset.filter(id__in=ids.split(","))
        data = []
        for item in queryset:
            data.append(
                {
                    "id": item.id,
                    "授信编号": item.code,
                    "授信名称": item.name,
                    "授信机构": item.organization,
                    "授信金额": item.amount,
                    "剩余金额": item.surplus_amount,
                    "集团董事会": item.group_chairman,
                    "集团党委会": item.group_deputy_chairman,
                    "子公司董事会": item.sub_chairman,
                    "子公司党委会": item.sub_deputy_chairman,
                    "起始日期": item.start_date,
                    "终止日期": item.end_date,
                    "备注": item.remark,
                }
            )
        df = pd.DataFrame(data)
        output = io.BytesIO()
        with pd.ExcelWriter(output) as wt:
            df.to_excel(wt, sheet_name="融资管理", index=False)
        return {"status": True, "msg": "导出成功", "data": output}
