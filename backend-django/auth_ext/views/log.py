from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from auth_ext.filters.log import AuthLogFilter
from auth_ext.models.log import AuthLog
from auth_ext.serializers.log import LogSerializer, LogDetailSerializer


class LogView(viewsets.ModelViewSet):
    serializer_class = LogSerializer
    queryset = AuthLog.objects.all()
    filterset_class = AuthLogFilter

    @action(detail=True, methods=["GET"])
    def log_detail(self, request, pk=None):
        log = self.get_object()
        serializer = LogDetailSerializer(log)
        return Response(serializer.data)
