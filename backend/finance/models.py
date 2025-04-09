import io

import pandas as pd
from django.core.paginator import Paginator
from django.db import models, transaction

from auth_ext.models import AuthExtUser
from credit.models import Credit
from generics.models import ImportExportRecord
from django.db.models import Manager


class Finance(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="贷款单位名称")
    type = models.IntegerField(verbose_name="贷款类型")
    "贷款金额"  # 贷款金额 为 授信可用贷款额度
    loan_amount = models.DecimalField(
        max_digits=15, decimal_places=2, verbose_name="贷款金额"
    )
    "还款金额"  # 还款金额 = 已经贷款loan金额之和
    repayment_amount = models.DecimalField(
        max_digits=15, decimal_places=2, verbose_name="还款金额"
    )
    "到期金额"  # 到期金额 = 贷款金额 - 已还款金额
    due_amount = models.DecimalField(
        max_digits=15, decimal_places=2, verbose_name="到期金额"
    )
    rate = models.DecimalField(
        max_digits=10, decimal_places=3, verbose_name="利率" "利率"
    )
    cost = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="综合成本")
    guaranty_type = models.IntegerField(verbose_name="担保类型")
    start_date = models.DateField(verbose_name="起始日期")
    end_date = models.DateField(verbose_name="结束日期")
    sign_date = models.DateField(verbose_name="签订时间")
    create_user = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="创建人"
    )
    dept = models.IntegerField(null=True, blank=True, verbose_name="部门")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "融资管理"
        managed = True
        db_table = "finance"

    def delete(self, using=None, keep_parents=False):
        with transaction.atomic(using=using):
            self.is_deleted = True
            self.save()

    @classmethod
    def export_data(
        cls, page=1, page_size=30, filter_dict={}, export_all=False, **kwargs
    ):
        queryset = cls.objects.filter(is_deleted=False, **filter_dict)
        if not export_all:
            paginator = Paginator(queryset, page_size)
            try:
                queryset = paginator.page(page)
            except:
                queryset = paginator.page(1)
        data = []
        for item in queryset:
            data.append(
                {
                    "id": item.id,
                    "贷款单位名称": item.name,
                    "贷款类型": item.type,
                    "授信金融机构": item.organization,
                    "授信总金额": item.amount,
                    "贷款余额": item.balance,
                    "利率": item.rate,
                    "综合成本": item.cost,
                    "担保类型": item.guaranty_type,
                    "起始日期": item.start_date.strftime("%Y-%m-%d"),
                    "结束日期": item.end_date.strftime("%Y-%m-%d"),
                    "创建时间": item.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "更新时间": item.update_time.strftime("%Y-%m-%d %H:%M:%S"),
                }
            )
        df = pd.DataFrame(data)
        output = io.BytesIO()
        with pd.ExcelWriter(output) as wt:
            df.to_excel(wt, sheet_name="融资管理", index=False)
        return {"status": True, "msg": "导出成功", "data": output}


"实际贷款情况"


class Loan(models.Model):
    "融资"
    id = models.AutoField(primary_key=True)
    credit = models.ForeignKey(
        Credit, on_delete=models.CASCADE, verbose_name="授信", related_name="finances"
    )
    "贷款单位名称"
    loan_unit = models.CharField(
        max_length=200, verbose_name="贷款单位名称", null=True, blank=True
    )
    name = models.CharField(max_length=200, verbose_name="贷款名称")
    type = models.CharField(max_length=200, verbose_name="贷款类型")
    "贷款金额"  # 贷款金额 为 授信可用贷款额度
    loan_amount = models.DecimalField(
        max_digits=15, decimal_places=2, verbose_name="贷款金额"
    )
    "已还金额"
    repay_amount = models.DecimalField(
        max_digits=15, decimal_places=2, verbose_name="已还金额"
    )
    "本金贷款利息"
    origin_interest_amount = models.DecimalField(
        max_digits=15, decimal_places=2, verbose_name="本金贷款利息", default=0
    )
    "已还利息"
    repay_interest = models.DecimalField(
        max_digits=15, decimal_places=2, verbose_name="已还利息", default=0
    )

    "贷款余额"
    loan_balance = models.DecimalField(
        max_digits=15, decimal_places=2, verbose_name="贷款余额"
    )
    "合同利率"
    contract_rate = models.DecimalField(
        max_digits=10, decimal_places=3, verbose_name="合同利率"
    )
    "综合利率"
    overall_rate = models.DecimalField(
        max_digits=10, decimal_places=3, verbose_name="综合利率"
    )
    "已做配存业务成本利率"
    deposit_rate = models.DecimalField(
        max_digits=10, decimal_places=3, verbose_name="已做配存业务成本利率"
    )
    "实际利率"
    actual_rate = models.DecimalField(
        max_digits=10, decimal_places=3, verbose_name="实际利率"
    )
    "是否固定利率"
    is_fixed_rate = models.BooleanField(default=False, verbose_name="是否固定利率")
    "保证金比例"
    margin_rate = models.DecimalField(
        max_digits=10, decimal_places=3, verbose_name="保证金比例"
    )
    "担保方式"
    guarantee_way = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="担保方式"
    )
    "提供担保的单位"
    guarantee_unit = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="提供担保的单位"
    )
    "反担保方式"
    anti_guarantee_way = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="反担保方式"
    )
    "反担保单位"
    anti_guarantee_unit = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="反担保单位"
    )
    "贷款借款日"
    loan_date = models.DateField(verbose_name="贷款借款日")
    "贷款到期日"
    due_date = models.DateField(verbose_name="贷款到期日")
    "利息"
    interest = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="利息")
    "是否配存业务"
    is_deposit = models.BooleanField(default=False, verbose_name="是否配存业务")
    "经办人"
    agent_user = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="经办人"
    )
    "债务文件"
    debt_file = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="债务文件"
    )
    "签订时间"
    sign_date = models.DateField(verbose_name="签订时间")
    "实际付息"
    actual_interest = models.DecimalField(
        max_digits=15, decimal_places=2, verbose_name="实际付息"
    )
    "备注"
    remark = models.TextField(null=True, blank=True, verbose_name="备注")
    dept = models.IntegerField(null=True, blank=True, verbose_name="部门")
    create_user = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="创建人"
    )
    update_user = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="更新人"
    )
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    external_loan: "Manager[ExternalLoan]"
    class Meta:
        db_table = "loan"
        managed = True
        verbose_name = "实际贷款情况"
        verbose_name_plural = verbose_name
        ordering = ["-id"]

    def delete(self, using=None, keep_parents=False):
        with transaction.atomic(using=using):
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
                    "贷款单位": item.name,
                    "贷款类型": item.type,
                    "授信金融机构": item.credit.organization,
                    "授信总金额": item.credit.amount,
                    "贷款金额": item.loan_amount,
                    "贷款余额": item.loan_balance,
                    "已还金额": item.repay_amount,
                    "本金贷款利息": item.origin_interest_amount,
                    "已还利息": item.repay_interest,
                    "合同利率": item.contract_rate,
                    "综合利率": item.overall_rate,
                    "已做配存业务成本利率": item.deposit_rate,
                    "实际利率": item.actual_rate,
                    "是否固定利率": item.is_fixed_rate,
                    "保证金比例": item.margin_rate,
                    "担保方式": item.guarantee_way,
                    "提供担保的单位": item.guarantee_unit,
                    "反担保方式": item.anti_guarantee_way,
                    "反担保单位": item.anti_guarantee_unit,
                    "贷款借款日": item.loan_date.strftime("%Y-%m-%d"),
                    "贷款到期日": item.due_date.strftime("%Y-%m-%d"),
                    "计息起始日": item.interest_start_date.strftime("%Y-%m-%d"),
                    "计息截止日": item.interest_end_date.strftime("%Y-%m-%d"),
                    "利息": item.interest,
                    "是否配存业务": item.is_deposit,
                    "经办人": item.agent_user,
                    "债务文件": item.debt_file,
                    "签订时间": item.sign_date.strftime("%Y-%m-%d"),
                    "实际付息": item.actual_interest,
                    "备注": item.remark,
                }
            )
        df = pd.DataFrame(data)
        output = io.BytesIO()
        with pd.ExcelWriter(output) as wt:
            df.to_excel(wt, sheet_name="融资管理", index=False)
        return {"status": True, "msg": "导出成功", "data": output}

"综合成本"
class ExternalLoan(models.Model):
    id = models.AutoField(primary_key=True)
    loan_id = models.IntegerField(verbose_name="实际贷款情况id")

    start_date = models.DateField(verbose_name="起始日期")
    end_date = models.DateField(verbose_name="结束日期")
    actual_cost = models.DecimalField(
        max_digits=15, decimal_places=2, verbose_name="实际付息"
    )
    create = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "external_loan"
        managed = True
        verbose_name = "综合成本"
        verbose_name_plural = verbose_name
        ordering = ["-id"]



"还款"


class LoanRepay(models.Model):
    "还款计划"
    loan = models.ForeignKey(
        Loan,
        on_delete=models.CASCADE,
        verbose_name="实际贷款情况",
        related_name="loan_repay",
    )
    "还款日期"
    repay_date = models.DateField(verbose_name="还款日期")
    "还款金额"
    repay_amount = models.DecimalField(
        max_digits=15, decimal_places=2, verbose_name="还款金额"
    )
    "会计凭证号"
    voucher_number = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="会计凭证号"
    )
    "偿还资金来源"
    repay_source = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="偿还资金来源"
    )
    "备注"
    remark = models.TextField(null=True, blank=True, verbose_name="备注")
    dept = models.IntegerField(null=True, blank=True, verbose_name="部门")
    create_user = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="创建人"
    )
    update_user = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="更新人"
    )
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "loan_repay"
        managed = True
        verbose_name = "还款计划"
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
                    "还款日期": item.repay_date.strftime("%Y-%m-%d"),
                    "还款金额": item.repay_amount,
                    "会计凭证号": item.voucher_number,
                    "偿还资金来源": item.repay_source,
                    "备注": item.remark,
                }
            )
        df = pd.DataFrame(data)
        output = io.BytesIO()
        with pd.ExcelWriter(output) as wt:
            df.to_excel(wt, sheet_name="还款计划", index=False)
        return {"status": True, "msg": "导出成功", "data": output}


"付息"


class LoanInterest(models.Model):
    "付息计划"
    loan = models.ForeignKey(
        Loan,
        on_delete=models.CASCADE,
        verbose_name="实际贷款情况",
        related_name="loan_interest",
    )
    "付息日期"
    interest_date = models.DateField(verbose_name="付息日期")
    "付息金额"
    interest_amount = models.DecimalField(
        max_digits=15, decimal_places=2, verbose_name="付息金额"
    )
    "会计凭证号"
    voucher_number = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="会计凭证号"
    )
    "偿还资金来源"
    interest_source = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="偿还资金来源"
    )
    "备注"
    remark = models.TextField(null=True, blank=True, verbose_name="备注")
    dept = models.IntegerField(null=True, blank=True, verbose_name="部门")
    create_user = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="创建人"
    )
    update_user = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="更新人"
    )
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "loan_interest"
        managed = True
        verbose_name = "付息计划"
        verbose_name_plural = verbose_name
        ordering = ["-id"]

    def delete(self, using=None, keep_parents=False):
        with transaction.atomic(using=using):
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
                    "付息日期": item.interest_date.strftime("%Y-%m-%d"),
                    "付息金额": item.interest_amount,
                    "会计凭证号": item.voucher_number,
                    "偿还资金来源": item.interest_source,
                    "备注": item.remark,
                }
            )
        df = pd.DataFrame(data)
        output = io.BytesIO()
        with pd.ExcelWriter(output) as wt:
            df.to_excel(wt, sheet_name="付息计划", index=False)
        return {"status": True, "msg": "导出成功", "data": output}
