from rest_framework import serializers

from auth_ext.models.media import FileMedia


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileMedia
        fields = '__all__'