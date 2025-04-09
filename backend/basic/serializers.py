from rest_framework import serializers

from basic.models import Basic


class BasicSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Basic
        fields = "__all__"
