import json
import time

from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin

from auth_ext.models.log import AuthLog
from fast.urls import MODULE_DICT


class LogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 将 request.body 缓存下来，供后续处理中使用
        if request.body:
            try:
                request.body_data = json.loads(request.body.decode("utf-8"))
            except json.JSONDecodeError:
                request.body_data = request.body.decode("utf-8")
        else:
            request.body_data = None
        start_time = time.time()
        request.start_time = start_time

    def process_response(self, request, response):
        # 获取请求的信息
        end_time = time.time()
        start_time = request.start_time
        takes_time = end_time - start_time
        user = request.user if request.user != AnonymousUser() else None
        path = request.get_full_path()
        method = request.method
        ip = request.META.get("REMOTE_ADDR", "未知")
        system = request.META.get("OS", "未知")
        browser = request.META.get("HTTP_USER_AGENT", "未知")
        body_data = request.body_data
        # 确定模块
        module = next(
            (value for key, value in MODULE_DICT.items() if key in path.split("/")), ""
        )

        if module:
            behavior = self.get_behavior(method, body_data, module)

            # Create AuthLog entry
            AuthLog.objects.create(
                user=user,
                module=f"{module}模块",
                ip=ip,
                method=method,
                url=path,
                address="address",  # Address logic needs to be implemented based on your requirements
                system=system,
                browser=browser,
                status=1 if response.status_code == 200 and user else 0,
                behavior=behavior,
                summary=f"{behavior}{module}",
                takes_time=takes_time,
                request_body=body_data if body_data else {},
                response_body=(
                    dict(json.loads(response.content.decode("utf-8")))
                    if response.content
                    else {}
                ),
                request_headers=dict(request.headers),
                response_headers=dict(response.headers),
            )
        return response

    def get_behavior(self, method, body_data, module):
        if method == "GET":
            return "查看"
        elif method == "POST":
            if module == "登录":
                return "登录"
            return body_data.get("behavior", "新增")
        elif method == "PUT":
            return "修改"
        elif method == "DELETE":
            return "删除"
        return "操作"
