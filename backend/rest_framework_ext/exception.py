from django.conf import settings
from rest_framework import status
from rest_framework.views import Response, exception_handler


# 错误处理（有错误）
def custom_exception_handler(err, context: dict):
    # 先调用REST framework默认的异常处理方法获得标准错误响应对象
    response: Response = exception_handler(err, context)
    if response is None:
        # 在DEBUG模式下不处理系统异常,如果处理后错误页面将变成标准格式
        if settings.DEBUG:
            raise err
        res = {"msg": f"服务器错误:{err}", "err_code": 500, "success": False}
        return Response(
            res, status=status.HTTP_500_INTERNAL_SERVER_ERROR, exception=True
        )
    else:
        msg = response.reason_phrase
        if "detail" in response.data:
            msg = response.data["detail"]
        else:
            for k, v in response.data.items():
                msg = v
                if isinstance(v, list):
                    msg = v[0]
        res = {}
        res.update(response.data)
        res["msg"] = msg
        res["code"] = response.status_code
        res["success"] = False
        return Response(res, status=status.HTTP_200_OK, exception=True)
