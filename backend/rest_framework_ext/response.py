from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


class CustomRenderer(JSONRenderer):
    # 重构render方法
    def render(self, data, accepted_media_type=None, renderer_context=None):
        try:
            # 默认的返回结构
            ret = {"data": data, "code": 0, "msg": "success", "success": True}

            # 封装信息
            if isinstance(data, dict):
                # restful风格返回数据
                if "list" in data:
                    msg = data.pop("msg", "success")
                    code = data.pop("code", 0)
                    success = data.pop("success", True)
                    ret = {"data": data, "code": code, "msg": msg, "success": success}
                else:
                    # restful 详情返回数据
                    ret["data"] = data
                    if all(key in data for key in ["code", "msg", "success"]):
                        ret["code"] = data["code"]
                        ret["msg"] = data["msg"]
                        ret["success"] = data["success"]
            elif isinstance(data, list):
                ret["data"] = data

            return super().render(ret, accepted_media_type, renderer_context)

        except Exception as e:
            # 处理异常
            error_ret = {"data": None, "code": -1, "msg": str(e), "success": False}
            return super().render(error_ret, accepted_media_type, renderer_context)
