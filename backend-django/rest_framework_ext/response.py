from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


class CustomRenderer(JSONRenderer):
    # 重构render方法
    def render(self, data, accepted_media_type=None, renderer_context=None):
        # 封装信息
        if isinstance(data, dict):
            msg = data.pop("msg", "success")
            code = data.pop("code", 0)
            success = data.pop("success", True)
        else:
            msg = "success"
            code = 0
            success = True
        ret = {"data": data, "code": code, "msg": msg, "success": success}
        return super().render(ret, accepted_media_type, renderer_context)
