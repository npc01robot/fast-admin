from datetime import timedelta, datetime

from celery import shared_task
from dateutil.relativedelta import relativedelta
from django.core.cache import cache
from django.db.models import Sum, F, Value
from django.db.models.functions import Coalesce, TruncMonth

from finance.models import Loan, LoanInterest, LoanRepay


def get_aggregate_amount(queryset):
    return queryset.aggregate(total_amount=Sum("loan_amount"))["total_amount"] or 0


# 总贷款
def get_loan_total_amount(refresh=False):
    CACHE_KEY = "loan_total_amount"
    total_amount = cache.get(CACHE_KEY)
    if not total_amount or refresh:
        queryset = Loan.objects.filter(is_deleted=False).all()
        total_amount = get_aggregate_amount(queryset)
        latest_amount_list = list(queryset.values_list("loan_amount", flat=True))[:10]

        # 发行债券
        bond_issue = get_aggregate_amount(queryset.filter(type="发行债券"))
        # 银行贷款
        bank_loan = get_aggregate_amount(queryset.filter(type="银行贷款"))
        # 一年期流贷
        one_year_mid_term = get_aggregate_amount(queryset.filter(type="一年期流贷"))
        # 中长期贷款
        long_term_loan = get_aggregate_amount(queryset.filter(type="中长期贷款"))
        # 非标业务
        non_standard = get_aggregate_amount(queryset.filter(type="非标业务"))
        # 农发行、国开行、进出口银行
        credit_loan = get_aggregate_amount(
            queryset.filter(credit__name__in=["农发行", "国开行", "进出口银行"])
        )
        # 项目贷款
        project_loan = get_aggregate_amount(queryset.filter(type="项目贷款"))

        # 低风险业务
        low_risk_loan = get_aggregate_amount(queryset.filter(type="低风险业务"))
        # 其他
        other = (
            total_amount
            - credit_loan
            - project_loan
            - long_term_loan
            - non_standard
            - low_risk_loan
        )
        total_amount = {
            "total_amount": total_amount,
            "latest_amount_list": latest_amount_list,
            "bond_issue": bond_issue,
            "bank_loan": bank_loan,
            "one_year_mid_term": one_year_mid_term,
            "long_term_loan": long_term_loan,
            "non_standard": non_standard,
            "credit_loan": credit_loan,
            "project_loan": project_loan,
            "low_risk_loan": low_risk_loan,
            "other": other,
            "percent": (
                latest_amount_list[-1] // (total_amount - latest_amount_list[-1])
                if latest_amount_list and total_amount
                else 0
            ),
        }
        cache.set(CACHE_KEY, total_amount, 24 * 60 * 60)
    return total_amount


# 近一年贷款
def get_one_year_loan_amount(refresh=False):
    CACHE_KEY = "one_year_loan_amount"
    one_year_amount = cache.get(CACHE_KEY)
    if not one_year_amount or refresh:
        one_year = Loan.objects.filter(
            due_date__lte=F("loan_date") + timedelta(days=365), is_deleted=False
        )
        one_year_list = list(one_year.values_list("loan_amount", flat=True))[:10]

        one_year_balance = get_aggregate_amount(one_year)
        # 银行贷款
        one_year_bank_loan = get_aggregate_amount(one_year.filter(type="银行贷款"))
        # 非标业务
        one_year_non_standard = get_aggregate_amount(one_year.filter(type="非标业务"))
        # 其他
        one_year_other = one_year_balance - one_year_bank_loan - one_year_non_standard
        one_year_amount = {
            "total_balance": one_year_balance,
            "latest_amount_list": one_year_list,
            "bank_loan": one_year_bank_loan,
            "non_standard": one_year_non_standard,
            "other": one_year_other,
            "percent": (
                one_year_list[-1] // (one_year_balance - one_year_list[-1])
                if one_year_list
                and one_year_balance
                and (one_year_balance - one_year_list[-1]) > 0
                else 0
            ),
        }
        cache.set(CACHE_KEY, one_year_amount, 24 * 60 * 60)
    return one_year_amount


# 中长期贷款
def get_long_term_loan_amount(refresh=False):
    CACHE_KEY = "long_term_loan_amount"
    long_term_amount = cache.get(CACHE_KEY)
    if not long_term_amount or refresh:
        long_term = Loan.objects.filter(
            due_date__gt=F("loan_date") + timedelta(days=365), is_deleted=False
        )
        long_term_list = list(long_term.values_list("loan_amount", flat=True))[:10]
        long_term_balance = get_aggregate_amount(long_term)
        # 中期流贷
        long_term_mid_term = get_aggregate_amount(long_term.filter(type="中期流贷"))
        # 项目贷款
        long_term_project_loan = get_aggregate_amount(long_term.filter(type="项目贷款"))
        # 发行债券
        long_term_bond_issue = get_aggregate_amount(long_term.filter(type="发行债券"))
        # 非标业务
        long_term_non_standard = get_aggregate_amount(long_term.filter(type="非标业务"))
        # 其他
        long_term_other = (
            long_term_balance
            - long_term_mid_term
            - long_term_project_loan
            - long_term_bond_issue
            - long_term_non_standard
        )
        long_term_amount = {
            "total_balance": long_term_balance,
            "latest_amount_list": long_term_list,
            "mid_term": long_term_mid_term,
            "project_loan": long_term_project_loan,
            "bond_issue": long_term_bond_issue,
            "non_standard": long_term_non_standard,
            "other": long_term_other,
            "percent": (
                long_term_list[-1] // (long_term_balance - long_term_list[-1])
                if long_term_list
                and long_term_balance
                and (long_term_balance - long_term_list[-1]) > 0
                else 0
            ),
        }
        cache.set(CACHE_KEY, long_term_amount, 24 * 60 * 60)
    return long_term_amount


# 一年内到期融资金额
def get_one_year_repayment_amount(refresh=False):
    CACHE_KEY = "one_year_repayment_amount"
    one_year_repayment = cache.get(CACHE_KEY)
    if not one_year_repayment or refresh:
        today = datetime.today()
        one_year_repayment = Loan.objects.filter(
            due_date__gte=today,
            due_date__lte=today + timedelta(days=365),
            is_deleted=False,
        )
        one_year_amount = get_aggregate_amount(one_year_repayment)
        one_year_repayment_list = list(
            one_year_repayment.values_list("loan_amount", flat=True)
        )[:10]
        one_year_repayment = {
            "total_balance": one_year_amount,
            "latest_amount_list": one_year_repayment_list,
            "percent": (
                one_year_repayment_list[-1]
                // (one_year_amount - one_year_repayment_list[-1])
                if one_year_repayment_list
                and one_year_amount
                and (one_year_amount - one_year_repayment_list[-1]) > 0
                else 0
            ),
        }
        cache.set(CACHE_KEY, one_year_repayment, 24 * 60 * 60)
    return one_year_repayment


@shared_task
def refresh_loan_cache():
    get_loan_total_amount(refresh=True)
    get_one_year_loan_amount(refresh=True)
    get_long_term_loan_amount(refresh=True)
    get_one_year_repayment_amount(refresh=True)


def get_interest_repay_data(refresh=False):
    # 近一年，每个月的数据之和,按月分组
    CACHE_KEY = "interest_repay_data"
    interest_repay_data = cache.get(CACHE_KEY)
    if not interest_repay_data or refresh:
        current_date = datetime.now().date()
        # 近一年的月份 除去本月
        months = [
            (current_date - relativedelta(months=i)).strftime("%Y-%m")
            for i in range(1, 13)  # 从当前月份的前一个月开始
        ][
            ::-1
        ]  # 反转顺序，得到从2022年10月到2023年9月
        one_year_ago = (datetime.now() - timedelta(days=365)).date()
        interest_data = (
            LoanInterest.objects.filter(
                is_deleted=False, interest_date__gte=one_year_ago
            )
            .annotate(year_month=TruncMonth("interest_date"))  # 按月截断
            .values("year_month")  # 选择按月计算的字段
            .annotate(total_amount=Sum("interest_amount"))  # 汇总每月的 interest_amount
            .order_by("year_month")
            .values("year_month", "total_amount")
        )

        interest_data_final = []
        formatted_interest_data = {
            item["year_month"].strftime("%Y-%m"): item["total_amount"]
            for item in interest_data
        }
        for month in months:
            if month in formatted_interest_data:
                interest_data_final.append(formatted_interest_data[month])
            else:
                interest_data_final.append(0)

        repay_data = (
            LoanRepay.objects.filter(is_deleted=False, repay_date__gte=one_year_ago)
            .annotate(year_month=TruncMonth("repay_date"))  # 按月截断
            .values("year_month")  # 选择按月计算的字段
            .annotate(total_amount=Sum("repay_amount"))  # 汇总每月的 repay_amount
            .values("year_month", "total_amount")
        )
        repay_data_final = []
        formatted_repay_data = {
            item["year_month"].strftime("%Y-%m"): item["total_amount"]
            for item in repay_data
        }
        for month in months:
            if month in formatted_repay_data:
                repay_data_final.append(formatted_repay_data[month])
            else:
                repay_data_final.append(0)

        interest_repay_data = {
            "interest_data": interest_data_final,
            "repay_data": repay_data_final,
            "date": months,
        }
        cache.set(CACHE_KEY, interest_repay_data, 30 * 24 * 60 * 60)
    return interest_repay_data


def get_loan_cache(refresh=True):
    loan_total_amount = get_loan_total_amount(refresh)
    one_year_loan_amount = get_one_year_loan_amount(refresh)
    long_term_loan_amount = get_long_term_loan_amount(refresh)
    one_year_repayment_amount = get_one_year_repayment_amount(refresh)
    interest_repay_data = get_interest_repay_data(refresh)
    return {
        "loan_total_amount": loan_total_amount,
        "one_year_loan_amount": one_year_loan_amount,
        "long_term_loan_amount": long_term_loan_amount,
        "one_year_repayment_amount": one_year_repayment_amount,
        "interest_repay_data": interest_repay_data,
    }
