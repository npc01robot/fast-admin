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


class LogDetailSerializer(LogSerializer):
    responseHeaders = serializers.JSONField(source="response_headers", read_only=True)
    requestHeaders = serializers.JSONField(source="request_headers", read_only=True)
    responseBody = serializers.JSONField(source="response_body", read_only=True)
    requestBody = serializers.JSONField(source="request_body", read_only=True)

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
            "responseHeaders",
            "requestHeaders",
            "responseBody",
            "requestBody",
        ]
