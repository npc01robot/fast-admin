import django_filters

from auth_ext.models.log import AuthLog


class AuthLogFilter(django_filters.FilterSet):
    class Meta:
        model = AuthLog
        fields = '__all__'