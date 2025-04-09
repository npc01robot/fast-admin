import logging
import os
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.utils import timezone

from generics.singles import post_upload_file
from generics.tasks import export_handler, upload_handle_task
from utils.storage import file_system_storage

logger = logging.getLogger(__name__)


class ImportExportRecord(models.Model):
    # 奇数为导入文件处理，偶数为导出文件处理
    UPLOAD_FILE = 1  # 仅上传文件

    DOWNLOAD_FILE = 2  # 仅下载文件
    CREDIT_EXPORT = 3  # 授信审批
    LOAN = 4  # 贷款审批
    REPAYMENT = 5  # 还款审批
    INTEREST = 6  # 利息审批
    GUARANTEE = 7  # 对外担保
    BE_GUARANTEE = 8  # 被担保信息
    BASIC_UPLOAD = 9  # 基础信息上传
    MODULE_CHOICES = (
        # 导入文件
        (UPLOAD_FILE, "文件上传"),
        # 导出文件
        (DOWNLOAD_FILE, "文件下载"),
        (CREDIT_EXPORT, "授信审批"),
        (LOAN, "贷款信息"),
        (REPAYMENT, "还本信息"),
        (INTEREST, "付息信息"),
        (GUARANTEE, "对外担保"),
        (BE_GUARANTEE, "被担保信息"),
    )
    module = models.IntegerField(
        default=1, choices=MODULE_CHOICES, verbose_name="模块类型"
    )
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
    status = models.IntegerField(
        default=STATUS_WAIT, choices=STATUS_CHOICES, verbose_name="处理状态"
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
        default=Decimal(0),
        editable=False,
        verbose_name="处理时长",
    )
    download_time = models.DateTimeField(
        null=True, editable=False, verbose_name="最后下载时间"
    )
    create_time = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name="创建时间"
    )
    download_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        editable=False,
        db_column="download_id",
        related_name="+",
        verbose_name="最后下载人",
    )
    create_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        editable=False,
        db_column="create_id",
        related_name="+",
        verbose_name="创建人",
    )
    complete_result = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="处理结果"
    )
    error_msg = models.CharField(
        max_length=200, null=True, editable=False, verbose_name="错误信息"
    )

    def __str__(self):
        return self.file_path

    class Meta:
        managed = True
        verbose_name = "上传下载文件记录"
        verbose_name_plural = "上传下载文件记录"
        ordering = ("-create_time",)
        db_table = "async_import_export_record"
        permissions = (
            ("upload_file", "上传文件"),
            ("download_file", "下载文件"),
            ("view_all_import_record", "查看所有人记录"),
        )

    # ========================================== 用户操作方法 ================================================
    @classmethod
    def op_create(cls, user, **validated_data):
        record = cls(create_user=user, **validated_data)
        record.save()
        return record

    def op_download(self, user):
        self.download_user = user
        self.download_time = timezone.now()
        self.save()

    def save_result(
        self,
        status=STATUS_COMPLETE,
        complete_result="处理完成",
        error_msg="",
        execute_time=0,
        complete_path="",
        **kwargs,
    ):
        self.status = status
        self.execute_time = execute_time
        self.complete_result = complete_result
        self.error_msg = error_msg
        self.complete_path = complete_path
        self.save()


@export_handler(module=ImportExportRecord.DOWNLOAD_FILE)
def get_file(module="finance", file_type="xlsx", **kwargs):
    from generics.class_factory import create_class

    class_name = kwargs.pop("class_name")
    instance = create_class(class_name)
    result = instance.export_data(**kwargs)
    if result["status"]:
        bio = result["data"]
        file_name = f'{module}{timezone.now().strftime("%S")}.{file_type}'
        file_path = os.path.join(
            "download",
            str(ImportExportRecord.DOWNLOAD_FILE),
            timezone.now().strftime("%Y%m%d"),
            file_name,
        )
        file_system_storage.mkdir(file_path)
        file_path = file_system_storage.get_available_name(file_path)
        save_path = file_system_storage.path(file_path)
        with open(save_path, "wb") as w:
            w.write(bio.getvalue())
        return {
            "module": ImportExportRecord.DOWNLOAD_FILE,
            "complete_path": file_path,
            "status": ImportExportRecord.STATUS_COMPLETE,
        }
    else:
        return {
            "module": ImportExportRecord.DOWNLOAD_FILE,
            "complete_path": "",
            "error_msg": result["msg"],
            "status": ImportExportRecord.STATUS_EXCEPTION,
        }


@receiver(signal=post_upload_file, sender=ImportExportRecord)
def post_upload_file_handler(sender, instance, **kwargs):
    if instance.module % 2 == 0:
        # 不处理文件下载
        return
    upload_handle_task(record_id=instance.pk)  # 上传文件的异步处理任务
