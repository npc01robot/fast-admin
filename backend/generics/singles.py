from django.dispatch import Signal

pre_merge_upload_file = Signal()
post_merge_upload_file = Signal()

post_upload_file = Signal()  # 文件上传成功后
http_requested = Signal()  # 收到http请求时
