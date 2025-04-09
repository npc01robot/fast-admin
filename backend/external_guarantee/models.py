import io

import pandas as pd
from django.db import models


class ExternalGuarantee(models.Model):
    id = models.AutoField(primary_key=True)
    be_guaranteed_unit = models.CharField(max_length=200, verbose_name="被担保单位")
    be_guaranteed_unit_parent = models.CharField(
        max_length=200, verbose_name="被担保单位母公司", blank=True, null=True
    )
    nature = models.CharField(
        max_length=200, verbose_name="单位性质", blank=True, null=True
    )
    ownership = models.CharField(
        max_length=200, verbose_name="产权关系", blank=True, null=True
    )
    item = models.TextField(verbose_name="担保事项", blank=True, null=True)
    method = models.CharField(
        max_length=200, verbose_name="担保方式", blank=True, null=True
    )
    start_date = models.DateField(verbose_name="担保开始日期", blank=True, null=True)
    end_date = models.DateField(verbose_name="担保结束日期", blank=True, null=True)
    amount = models.DecimalField(
        max_digits=15, decimal_places=2, verbose_name="担保金额", blank=True, null=True
    )
    application_file = models.CharField(
        max_length=200, verbose_name="申请担保函", blank=True, null=True
    )
    "担保单位"
    guarantee_unit = models.CharField(
        max_length=200, verbose_name="担保单位", blank=True, null=True
    )

    group_date = models.DateField(verbose_name="集团董事会日期", blank=True, null=True)
    group_decision_file = models.CharField(
        max_length=200, verbose_name="集团董事会决议", blank=True, null=True
    )
    "国资委备案金额"
    sasac_record_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="国资委备案金额",
        blank=True,
        null=True,
    )
    "国资委备案表"
    sasac_record_file = models.CharField(
        max_length=200, verbose_name="国资委备案表", blank=True, null=True
    )
    receipt_date = models.DateField(verbose_name="收函日期", blank=True, null=True)
    receipt_amount = models.DecimalField(
        max_digits=15, decimal_places=2, verbose_name="收函金额", blank=True, null=True
    )

    remark = models.TextField(verbose_name="备注", blank=True, null=True)
    create_user = models.CharField(
        max_length=200, verbose_name="创建人", blank=True, null=True
    )
    update_user = models.CharField(
        max_length=200, verbose_name="更新人", blank=True, null=True
    )
    dept = models.IntegerField(verbose_name="所属部门", blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = "external_guarantee"
        verbose_name = "对外担保"
        verbose_name_plural = verbose_name

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    @classmethod
    def export_data(
        cls, page=1, page_size=30, filter_dict={}, export_all=False, **kwargs
    ):
        queryset = cls.objects.filter(is_deleted=False, **filter_dict)
        # if not export_all:
        #     paginator = Paginator(queryset, page_size)
        #     try:
        #         queryset = paginator.page(page)
        #     except:
        #         queryset = paginator.page(1)
        ids = kwargs.get("ids")
        if ids:
            queryset = queryset.filter(id__in=ids.split(","))
        data = []
        for item in queryset:
            data.append(
                {
                    "id": item.id,
                    "被担保单位": item.be_guaranteed_unit,
                    "被担保单位母公司": item.be_guaranteed_unit_parent,
                    "单位性质": item.nature,
                    "产权关系": item.ownership,
                    "担保事项": item.item,
                    "担保方式": item.method,
                    "担保开始日期": item.start_date,
                    "担保结束日期": item.end_date,
                    "担保金额": item.amount,
                    "申请担保函": item.application_file,
                    "担保单位": item.guarantee_unit,
                    "集团董事会日期": item.group_date,
                    "集团董事会决议": item.group_decision_file,
                    "收函日期": item.receipt_date,
                    "收函金额": item.receipt_amount,
                    "备注": item.remark,
                    "创建人": item.create_user,
                    "更新人": item.update_user,
                    "创建时间": item.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "更新时间": item.update_time.strftime("%Y-%m-%d %H:%M:%S"),
                }
            )
        df = pd.DataFrame(data)
        output = io.BytesIO()
        with pd.ExcelWriter(output) as wt:
            df.to_excel(wt, sheet_name="付息计划", index=False)
        return {"status": True, "msg": "导出成功", "data": output}


# 被担保单位
class ExternalBeGuaranteed(models.Model):
    id = models.AutoField(primary_key=True)
    guarantee_unit = models.CharField(
        max_length=200, verbose_name="担保单位", blank=True, null=True
    )
    guarantee_parent = models.CharField(
        max_length=200, verbose_name="担保单位母公司", blank=True, null=True
    )
    nature = models.CharField(
        max_length=200, verbose_name="单位性质", blank=True, null=True
    )
    ownership = models.CharField(
        max_length=200, verbose_name="产权关系", blank=True, null=True
    )
    item = models.TextField(verbose_name="担保事项", blank=True, null=True)
    method = models.CharField(
        max_length=200, verbose_name="担保方式", blank=True, null=True
    )
    start_date = models.DateField(verbose_name="被担保开始日期", blank=True, null=True)
    end_date = models.DateField(verbose_name="被担保结束日期", blank=True, null=True)
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="被担保金额",
        blank=True,
        null=True,
    )
    application_file = models.CharField(
        max_length=200, verbose_name="申请担保函", blank=True, null=True
    )
    be_guaranteed_unit = models.CharField(
        max_length=200, verbose_name="被担保单位", blank=True, null=True
    )
    group_date = models.DateField(verbose_name="集团董事会日期", blank=True, null=True)
    group_decision_file = models.CharField(
        max_length=200, verbose_name="集团董事会决议", blank=True, null=True
    )
    "国资委备案金额"
    sasac_record_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="国资委备案金额",
        blank=True,
        null=True,
    )
    "国资委备案表"
    sasac_record_file = models.CharField(
        max_length=200, verbose_name="国资委备案表", blank=True, null=True
    )
    receipt_date = models.DateField(verbose_name="收函日期", blank=True, null=True)
    receipt_amount = models.DecimalField(
        max_digits=15, decimal_places=2, verbose_name="收函金额", blank=True, null=True
    )

    remark = models.TextField(verbose_name="备注", blank=True, null=True)
    dept = models.IntegerField(verbose_name="所属部门", blank=True, null=True)
    create_user = models.CharField(
        max_length=200, verbose_name="创建人", blank=True, null=True
    )
    update_user = models.CharField(
        max_length=200, verbose_name="更新人", blank=True, null=True
    )
    is_deleted = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = "external_be_guaranteed"
        verbose_name = "被担保单位"
        verbose_name_plural = verbose_name

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    @classmethod
    def export_data(
        cls, page=1, page_size=30, filter_dict={}, export_all=False, **kwargs
    ):
        queryset = cls.objects.filter(is_deleted=False, **filter_dict)
        # if not export_all:
        #     paginator = Paginator(queryset, page_size)
        #     try:
        #         queryset = paginator.page(page)
        ids = kwargs.get("ids")
        if ids:
            queryset = queryset.filter(id__in=ids.split(","))
        data = []
        for item in queryset:
            data.append(
                {
                    "id": item.id,
                    "担保单位": item.guarantee_unit,
                    "担保单位母公司": item.guarantee_parent,
                    "单位性质": item.nature,
                    "产权关系": item.ownership,
                    "担保事项": item.item,
                    "担保方式": item.method,
                    "被担保开始日期": item.start_date,
                    "被担保结束日期": item.end_date,
                    "被担保金额": item.amount,
                    "申请担保函": item.application_file,
                    "被担保单位": item.be_guaranteed_unit,
                    "集团董事会日期": item.group_date,
                    "集团董事会决议": item.group_decision_file,
                    "收函日期": item.receipt_date,
                    "收函金额": item.receipt_amount,
                    "备注": item.remark,
                    "创建人": item.create_user,
                    "更新人": item.update_user,
                    "创建时间": item.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "更新时间": item.update_time.strftime("%Y-%m-%d %H:%M:%S"),
                }
            )
        df = pd.DataFrame(data)
        output = io.BytesIO()
        with pd.ExcelWriter(output) as wt:
            df.to_excel(wt, sheet_name="付息计划", index=False)
        return {"status": True, "msg": "导出成功", "data": output}
