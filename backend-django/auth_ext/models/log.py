from django.db import models

from fast import settings


class AuthLog(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    module = models.CharField(max_length=200)
    ip = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    method = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    system = models.CharField(max_length=200)
    browser = models.CharField(max_length=200)
    status = models.IntegerField(choices=((1, '成功'), (0, '失败')))
    behavior = models.CharField(max_length=200)
    action_time = models.DateTimeField(auto_now_add=True)
    summary = models.CharField(max_length=1000)
    body = models.TextField(max_length=2000)
    takes_time = models.IntegerField(default=0)
    class Meta:
        db_table = 'auth_ext_log'
        verbose_name = "用户日志"
        managed = True
