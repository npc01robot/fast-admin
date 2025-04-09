from rest_framework import serializers

from auth_ext.models import AuthExtUser
from auth_ext.models.department import Department
from external_guarantee.models import ExternalGuarantee, ExternalBeGuaranteed


class ExternalGuaranteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalGuarantee
        fields = "__all__"

    def create(self, validated_data):
        user:AuthExtUser = self.context["request"].user
        if user.dept:
            dept = Department().get_top_departments(user.dept)
            validated_data["dept"] = dept.id
        return super().create(validated_data)

class ExternalBeGuaranteedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalBeGuaranteed
        fields = "__all__"

    def create(self, validated_data):
        user:AuthExtUser = self.context["request"].user
        if user.dept:
            dept = Department().get_top_departments(user.dept)
            validated_data["dept"] = dept.id
        return super().create(validated_data)