from django_filters import FilterSet
from basic.models import Basic


class BaseFilterSet(FilterSet):

    class Meta:
        model = Basic
        fields = [
            "type",
        ]
