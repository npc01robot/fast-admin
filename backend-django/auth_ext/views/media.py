from datetime import datetime

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from auth_ext.models.media import FileMedia
from utils.storage import save_download_file


class MediaFileViewSet(viewsets.GenericViewSet):

    @action(detail=False, methods=['post'])
    def upload(self, request):
        user = request.user
        file = request.FILES.get('file')
        filename = request.data.get('filename')
        file_path = save_download_file(filename,file)

        FileMedia.objects.create(
            user=user,
            path=file_path
        )
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['GET'])
    def get_file_list(self, request):
        user = request.user
        file_list = FileMedia.objects.filter(user=user).values('path')
        return Response({'file_list': file_list})
