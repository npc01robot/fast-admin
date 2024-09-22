from rest_framework import viewsets

from auth_ext.filters.log import AuthLogFilter
from auth_ext.models.log import AuthLog
from auth_ext.serializers.log import LogSerializer


class LogView(viewsets.ModelViewSet):
    serializer_class = LogSerializer
    queryset = AuthLog.objects.all()
    filterset_class = AuthLogFilter
