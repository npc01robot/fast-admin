from auth_ext.models.department import Department
from rest_framework import serializers


class DepartmentSerializer(serializers.ModelSerializer):
    parent_id = serializers.SerializerMethodField()

    def get_parent_id(self, obj):
        if obj.parent:
            return obj.parent.id
        else:
            return None

    class Meta:
        model = Department
        fields = [
            "id",
            "name",
            "parent_id",
            "sort",
            "phone",
            "email",
            "type",
            "description",
            "remark",
            "status",
            "is_delete",
            "create_time",
            "update_time",
        ]
