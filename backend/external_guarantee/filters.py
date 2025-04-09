from django_filters import FilterSet
import re
from django_filters.rest_framework import filters
from external_guarantee.models import ExternalGuarantee, ExternalBeGuaranteed


class ExternalGuaranteeFilter(FilterSet):
    guarantee_unit = filters.CharFilter(method="multi_re_filter")
    be_guaranteed_unit = filters.CharFilter(method="multi_re_filter")
    start_date_after = filters.DateFilter(field_name="start_date", lookup_expr="gte")
    start_date_before = filters.DateFilter(field_name="start_date", lookup_expr="lte")
    end_date_after = filters.DateFilter(field_name="end_date", lookup_expr="gte")
    end_date_before = filters.DateFilter(field_name="end_date", lookup_expr="lte")

    @staticmethod
    def re_split_value(value: str) -> set:
        return set(v for v in re.split(r"[,;，；\s]\s*", str(value)) if v.strip())

    def multi_re_filter(self, queryset, name, value):
        """支持前端传多个值, 以逗号, 空格, 分号换行等分隔"""
        values = self.re_split_value(value)
        if values:
            return queryset.filter(**{"{}__in".format(name): values})
        return queryset

    class Meta:
        model = ExternalGuarantee
        fields = "__all__"


class ExternalBeGuaranteedFilter(FilterSet):
    guarantee_unit = filters.CharFilter(method="multi_re_filter")
    be_guaranteed_unit = filters.CharFilter(method="multi_re_filter")
    start_date_after = filters.DateFilter(field_name="start_date", lookup_expr="gte")
    start_date_before = filters.DateFilter(field_name="start_date", lookup_expr="lte")
    end_date_after = filters.DateFilter(field_name="end_date", lookup_expr="gte")
    end_date_before = filters.DateFilter(field_name="end_date", lookup_expr="lte")

    @staticmethod
    def re_split_value(value: str) -> set:
        return set(v for v in re.split(r"[,;，；\s]\s*", str(value)) if v.strip())

    def multi_re_filter(self, queryset, name, value):
        """支持前端传多个值, 以逗号, 空格, 分号换行等分隔"""
        values = self.re_split_value(value)
        if values:
            return queryset.filter(**{"{}__in".format(name): values})
        return queryset

    class Meta:
        model = ExternalBeGuaranteed
        fields = "__all__"
