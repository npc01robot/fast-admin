from rest_framework import serializers

from auth_ext.models.log import AuthLog


class LogSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    takesTime = serializers.FloatField(source="takes_time", read_only=True)

    class Meta:
        model = AuthLog
        fields = [
            "id",
            "username",
            "ip",
            "address",
            "browser",
            "action_time",
            "summary",
            "status",
            "method",
            "url",
            "module",
            "system",
            "takesTime",
        ]
