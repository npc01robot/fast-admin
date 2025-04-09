from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from basic.filters import BaseFilterSet
from basic.models import Basic
from basic.serializers import BasicSerializer
from basic.tasks import upload_basic_upload
from generics.models import ImportExportRecord
from generics.tasks import upload_handle_task
from utils.excel import export_template
from utils.storage import file_system_storage, save_temp_file


class BasicViewSet(viewsets.ModelViewSet):
    queryset = Basic.objects.filter(is_deleted=False).all()
    serializer_class = BasicSerializer
    filterset_class = BaseFilterSet
    pagination_class = None

    @action(detail=False, methods=["get"])
    def excel_template(self, request):
        type = int(request.query_params.get("type"))
        cn_name = Basic.TYPE_CHOICES[type - 1][1]

        headers = ["编号", "名称", "上级编号", "排序（0-9）", "备注"]
        # content = [
        #     [1,"测试名称1","",0,"备注1"],
        #     [2,"测试名称2",1,1,"备注2"],
        #     [3,"测试名称3",1,2,"备注3"],
        #     ]
        # 导入模版
        result = export_template(cn_name, headers)
        bio = result.get("data")
        file_path = save_temp_file(f"{cn_name}_导入模版.xlsx", bio)
        complete_url = file_system_storage.url(file_path)
        return Response({"url": complete_url})

    # 导入excel文件
    @action(detail=False, methods=["post"])
    def excel(self, request):
        file = request.data.get("base64")
        basic_type = request.data.get("type")
        # 处理数据
        result = upload_basic_upload(
            file,
            basic_type,
        )
        return Response(result)
