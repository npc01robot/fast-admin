# 文件导出列表显示
from django.core.paginator import Paginator
from rest_framework import generics, serializers, status
from rest_framework.response import Response

from fast.settings import BASE_URL
from generics.models import ImportExportRecord
from generics.serializers import ImportExportRecordSerializer
from utils.storage import save_upload_base64_file, file_system_storage


class ImportExportRecordView(generics.ListAPIView):
    """
    导入导出记录列表
    """

    queryset = ImportExportRecord.objects.all()
    serializer_class = ImportExportRecordSerializer
    pagination_class = Paginator

    def list(self, request, *args, **kwargs):
        user = request.user
        query_params = request.query_params.dict()
        show_all = query_params.get("all", False)
        queryset = self.get_queryset()
        if not show_all:
            queryset = queryset.filter(create_user=user)
        page = int(query_params.get("page", 1))
        page_size = int(query_params.get("page_size", 10))
        status = query_params.get("status", None)
        type = query_params.get("type", None)
        if status:
            queryset = queryset.filter(status=status)
        if type:
            queryset = queryset.filter(module=type)
        paginator = Paginator(queryset, page_size)
        try:
            queryset = paginator.page(page)
        except:
            queryset = paginator.page(1)
        data = self.serializer_class(queryset, many=True).data
        return Response(
            {
                "total": paginator.count,
                "page": page,
                "page_size": page_size,
                "page_count": paginator.num_pages,
                "list": data,
            }
        )


class ImportExportTypeView(generics.ListAPIView):
    def list(self, request, *args, **kwargs):
        choices = ImportExportRecord.MODULE_CHOICES
        data = [{"value": i[0], "label": i[1]} for i in choices]
        return Response(data)


class UploadFileView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        file = request.data.get("base64")
        file_name = request.data.get("filename")
        file_path = save_upload_base64_file(file, file_name)
        file_path = file_system_storage.url(file_path)
        file_url = file_system_storage.url(file_path)
        return Response(
            {"file_url": file_url, "file_path": file_path}, status=status.HTTP_200_OK
        )
