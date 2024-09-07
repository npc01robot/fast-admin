from auth_ext.models.department import Department
from rest_framework import serializers


class DepartmentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Department
        fields = "__all__"