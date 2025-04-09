import datetime

from rest_framework import serializers

from auth_ext.models import AuthExtUser
from auth_ext.models.department import Department
from credit.models import Credit


class CreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credit
        fields = "__all__"

    def validate(self, data):
        if data.get("code"):
            return data
        date = datetime.datetime.now().strftime("%Y%m%d")
        credit = Credit.objects.last()
        credit_id = credit.id if credit else 0
        last_code = str(credit_id)
        last_code = last_code[-4:].zfill(4)
        data["code"] = "SX_" + date + last_code
        return data

    def create(self, validated_data):
        user:AuthExtUser = self.context["request"].user
        if user.dept:
            dept = Department().get_top_departments(user.dept)
            validated_data["dept"] = dept.id
        return Credit.objects.create(**validated_data)