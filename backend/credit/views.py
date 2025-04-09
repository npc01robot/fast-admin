from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from auth_ext.models.department import Department
from credit.filters import CreditFilter
from credit.models import Credit
from credit.serializers import CreditSerializer
from generics.models import ImportExportRecord
from generics.tasks import export_handle_task


class CreditViewSet(viewsets.ModelViewSet):
    queryset = Credit.objects.filter(is_deleted=False).all()
    serializer_class = CreditSerializer
    filterset_class = CreditFilter


    def get_queryset(self):
        user = self.request.user
        if user.dept:
            dept_top = Department().get_top_departments(user.dept)
            return self.queryset.filter(dept=dept_top.id)
        else:
            return self.queryset.all()

    @action(detail=False, methods=["get"])
    def export(self, request, *args, **kwargs):
        user = request.user
        query_params = request.query_params.dict()

        export_handle_task.delay(
            ImportExportRecord.CREDIT_EXPORT,
            user.id,
            **query_params,
            class_name="Credit",
        )
        return Response({"message": "Export task has been submitted."})
