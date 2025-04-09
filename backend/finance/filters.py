import re

from django_filters import FilterSet
from django_filters.rest_framework import filters

from finance.models import Finance, Loan, LoanRepay, LoanInterest


class FinanceFilter(FilterSet):
    name = filters.CharFilter(lookup_expr="contains")

    class Meta:
        model = Finance
        fields = "__all__"


class LoanFilter(FilterSet):
    loan_unit = filters.CharFilter(method="multi_re_filter")
    type = filters.CharFilter(method="multi_re_filter")
    credit_organization = filters.CharFilter(
        field_name="credit__organization", method="multi_re_filter"
    )
    loan_date_before = filters.DateFilter(field_name="loan_date", lookup_expr="lte")
    loan_date_after = filters.DateFilter(field_name="loan_date", lookup_expr="gte")
    due_date_before = filters.DateFilter(field_name="due_date", lookup_expr="lte")
    due_date_after = filters.DateFilter(field_name="due_date", lookup_expr="gte")
    interest_start_date_before = filters.DateFilter(
        field_name="interest_start_date", lookup_expr="lte"
    )
    interest_start_date_after = filters.DateFilter(
        field_name="interest_start_date", lookup_expr="gte"
    )

    class Meta:
        model = Loan
        fields = "__all__"

    @staticmethod
    def re_split_value(value: str) -> set:
        return set(v for v in re.split(r"[,;，；\s]\s*", str(value)) if v.strip())

    def multi_re_filter(self, queryset, name, value):
        """支持前端传多个值, 以逗号, 空格, 分号换行等分隔"""
        values = self.re_split_value(value)
        if values:
            return queryset.filter(**{"{}__in".format(name): values})
        return queryset


class LoanRepayFilter(FilterSet):
    loan_unit = filters.CharFilter(
        field_name="loan__loan_unit", method="multi_re_filter"
    )
    loan_type = filters.CharFilter(field_name="loan__type", method="multi_re_filter")
    sign_date_before = filters.DateFilter(
        field_name="loan__sign_date", lookup_expr="lte"
    )
    sign_date_after = filters.DateFilter(
        field_name="loan__sign_date", lookup_expr="gte"
    )
    due_date_before = filters.DateFilter(field_name="loan__due_date", lookup_expr="lte")
    due_date_after = filters.DateFilter(field_name="loan__due_date", lookup_expr="gte")
    repay_date_before = filters.DateFilter(field_name="repay_date", lookup_expr="lte")
    repay_date_after = filters.DateFilter(field_name="repay_date", lookup_expr="gte")

    class Meta:
        model = LoanRepay
        fields = "__all__"

    @staticmethod
    def re_split_value(value: str) -> set:
        return set(v for v in re.split(r"[,;，；\s]\s*", str(value)) if v.strip())

    def multi_re_filter(self, queryset, name, value):
        """支持前端传多个值, 以逗号, 空格, 分号换行等分隔"""
        values = self.re_split_value(value)
        if values:
            return queryset.filter(**{"{}__in".format(name): values})
        return queryset


class LoanInterestFilter(FilterSet):
    loan_unit = filters.CharFilter(
        field_name="loan__loan_unit", method="multi_re_filter"
    )
    loan_type = filters.CharFilter(field_name="loan__type", method="multi_re_filter")
    sign_date_before = filters.DateFilter(
        field_name="loan__sign_date", lookup_expr="lte"
    )
    sign_date_after = filters.DateFilter(
        field_name="loan__sign_date", lookup_expr="gte"
    )
    due_date_before = filters.DateFilter(field_name="loan__due_date", lookup_expr="lte")
    due_date_after = filters.DateFilter(field_name="loan__due_date", lookup_expr="gte")
    interest_date_before = filters.DateFilter(
        field_name="repay_date", lookup_expr="lte"
    )
    interest_date_after = filters.DateFilter(field_name="repay_date", lookup_expr="gte")

    class Meta:
        model = LoanInterest
        fields = "__all__"

    @staticmethod
    def re_split_value(value: str) -> set:
        return set(v for v in re.split(r"[,;，；\s]\s*", str(value)) if v.strip())

    def multi_re_filter(self, queryset, name, value):
        """支持前端传多个值, 以逗号, 空格, 分号换行等分隔"""
        values = self.re_split_value(value)
        if values:
            return queryset.filter(**{"{}__in".format(name): values})
        return queryset
