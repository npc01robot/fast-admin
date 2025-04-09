from __future__ import absolute_import, unicode_literals


import os
from celery import Celery, Task, shared_task

from fast import settings

# 设置环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fast.settings")
# 实例化
app = Celery(
    "fast", broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND
)
app.autodiscover_tasks()


# 一个测试任务
@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
