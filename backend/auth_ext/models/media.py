from celery import shared_task
from django.db import models

from auth_ext.models import AuthExtUser


class FileMedia(models.Model):
    id = models.AutoField(primary_key=True)

    STATUS_WAIT = 0  # 待处理
    STATUS_COMPLETE = 1  # 处理完成
    STATUS_PROCESS = 2  # 处理中
    STATUS_EXCEPTION = 3  # 处理异常
    STATUS_CHOICES = (
        (STATUS_WAIT, "待处理"),
        (STATUS_COMPLETE, "处理完成"),
        (STATUS_PROCESS, "处理中"),
        (STATUS_EXCEPTION, "处理异常"),
    )
    # 保存导入文件
    file_path = models.CharField(
        max_length=256, null=True, editable=False, verbose_name="导入文件路径"
    )

    # 保存导出文件, 异常处理结果文件, 对应前端处理结果下载
    complete_path = models.CharField(
        max_length=256, null=True, editable=False, verbose_name="处理结果文件路径"
    )

    execute_time = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        editable=False,
        verbose_name="处理时长",
    )
    user = models.ForeignKey(
        AuthExtUser, null=True, related_name="files", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    status = models.IntegerField(
        default=STATUS_WAIT, choices=STATUS_CHOICES, verbose_name="处理状态"
    )
    complete_result = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="处理结果"
    )
    error_msg = models.CharField(
        max_length=200, null=True, editable=False, verbose_name="错误信息"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "file_media"
        managed = True
