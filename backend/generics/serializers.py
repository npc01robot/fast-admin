from rest_framework import serializers

from generics.models import ImportExportRecord
from utils.storage import file_system_storage


class ImportExportRecordSerializer(serializers.ModelSerializer):
    module = serializers.SerializerMethodField()
    complete_path = serializers.SerializerMethodField()

    def get_complete_path(self, obj):
        return file_system_storage.url(obj.complete_path)

    def get_module(self, obj):
        dict_module = dict(ImportExportRecord.MODULE_CHOICES)
        return dict_module[obj.module]

    class Meta:
        model = ImportExportRecord
        fields = "__all__"
