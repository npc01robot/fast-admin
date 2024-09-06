from auth_ext.models.department import Department
from auth_ext.serializers.department import DepartmentSerializer
from rest_framework import viewsets


class DepartmentViewSet(viewsets.ModelViewSet):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()
    permission_classes = []
