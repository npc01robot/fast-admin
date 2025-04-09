import logging
import os
from time import perf_counter

import pandas as pd
from celery import shared_task
from django.dispatch import receiver
from django.utils import timezone


__all__ = ["upload_handler", "export_handler", "export_handle_task"]

from generics.singles import post_upload_file
from utils.storage import file_system_storage


class AsyncTaskDispatcher:
    """
    异步任务调度类： 通过 dispatch_id 唯一标识一个 同步处理函数
    """

    def __init__(self, name):
        self.name = name
        self._handlers = {}

    @property
    def handlers(self):
        return self._handlers

    def connect(self, handler, dispatch_id):
        logging.info(f"Handler {handler} append to async task dispatcher<{self.name}>")
        self._handlers[dispatch_id] = handler

    def handle(self, dispatch_id, *args, **kwargs):
        handler = self.handlers.get(dispatch_id, None)
        if handler is None:
            raise Exception(f"dispatch_id {dispatch_id} does not match any handler!")
        return handler(*args, **kwargs)


_upload_task = AsyncTaskDispatcher("upload")  # 文件上传异步任务处理调度器
_export_task = AsyncTaskDispatcher("export")  # 文件导出异步任务处理调度器


@shared_task
def upload_handle_task(record_id, **kwargs):
    """
    文件上传异步处理任务，调度通过`upload_handler`装饰器装饰过的同步函数；
        该实现目的是为了同步异步分离，各业务模块的开发人员只需要关注同步函数功能的实现，不需要过多的修改配置调试异步
    :param record_id: 上传记录id
    :param kwargs: 附加参数
    :return:
    """
    from generics.models import ImportExportRecord

    record_obj = ImportExportRecord.objects.filter(pk=record_id).first()
    if not record_obj:
        return
    dispatch_id = record_obj.module
    file_path = record_obj.file_path
    assert file_path
    if file_system_storage.exists(file_path):
        file_path = file_system_storage.path(file_path)
    kwargs.update(
        {
            "user": record_obj.create_user,
            "file_path": file_path,
        }
    )
    record_obj.status = ImportExportRecord.STATUS_PROCESS
    record_obj.save()

    time_begin = perf_counter()

    try:
        result = _upload_task.handle(dispatch_id=dispatch_id, **kwargs) or {}
    except Exception as e:
        result = {"error_msg": str(e), "status": ImportExportRecord.STATUS_EXCEPTION}

    if result.get("error_msg"):
        # 保存错误信息
        if result.get("error_type"):
            error_file_path = save_error_message_data(
                record_obj.get_module_display(), result["error_type"]
            )
            result.pop("error_type")
        else:
            error_file_path = save_error_message(
                record_obj.get_module_display(), result["error_msg"]
            )

        if isinstance(result["error_msg"], str):
            # 如果error_msg为字符串, 默认为代码raise出来的错误, 限制长度200
            result["error_msg"] = result["error_msg"][:200]
        else:
            # 如果error_msg为列表, 默认为逻辑处理错误, 不保存到数据库
            result.pop("error_msg")

        result.update(
            {
                "complete_path": error_file_path,
                "status": ImportExportRecord.STATUS_EXCEPTION,
            }
        )

    time_end = perf_counter()

    result["execute_time"] = time_end - time_begin
    record_obj.save_result(**result)


def upload_handler(module):
    """
    注册文件上传处理处理函数的装饰器
    使用：

        @upload_handler(module=ImportExportRecord.UPLOAD_FILE)
        def deal_upload_file(file_path, *args, **kwargs):
            # 处理逻辑
            return {'status': ImportExportRecord.STATUS_COMPLETE, 'complete_result': '文件上传成功'}

    :param module: 模块id
    :return: 处理结果dict，用于写入`ImportExportRecord.save_result()`
            { 'status': 处理状态,
            'complete_result': 处理结果,
            'error_msg': 错误信息 [{}...],用于生成错误文件
            'complete_path': 结果文件路径 }
    """

    def _decorator(func):
        if isinstance(module, (list, tuple)):
            for m in module:
                _upload_task.connect(handler=func, dispatch_id=m)
        else:
            _upload_task.connect(handler=func, dispatch_id=module)
        return func

    return _decorator


def export_handler(module):
    """
    注册文件导出处理处理函数的装饰器
    :param module:
    :return:
    """

    def _decorator(func):
        if isinstance(module, (list, tuple)):
            for m in module:
                _export_task.connect(handler=func, dispatch_id=m)
        else:
            _export_task.connect(handler=func, dispatch_id=module)
        return func

    return _decorator


@shared_task
def export_handle_task(module, user_id, **kwargs):
    """
    文件导出异步处理任务，调度通过`export_handler`装饰器装饰过的同步函数；
        该实现目的是为了同步异步分离，各业务模块的开发人员只需要关注同步函数功能的实现，不需要过多的修改配置调试异步
    :param user_id:
    :param module:
    :param kwargs: 附加参数
    :return:
    """
    from generics.models import ImportExportRecord

    record_obj = ImportExportRecord(module=module, create_user_id=user_id)
    dispatch_id = ImportExportRecord.DOWNLOAD_FILE  # 默认下载文件
    kwargs.update({"user_id": user_id})
    record_obj.status = ImportExportRecord.STATUS_PROCESS
    record_obj.save()

    time_begin = perf_counter()

    try:
        result = _export_task.handle(dispatch_id=dispatch_id, **kwargs) or {}

    except Exception as e:
        result = {"error_msg": str(e), "status": ImportExportRecord.STATUS_EXCEPTION}

    if result.get("error_msg"):
        # 保存错误信息
        if result.get("error_type"):
            error_file_path = save_error_message_data(
                record_obj.get_module_display(), result["error_type"]
            )
            result.pop("error_type")
        else:
            error_file_path = save_error_message(
                record_obj.get_module_display(), result["error_msg"]
            )

        if isinstance(result["error_msg"], str):
            # 如果error_msg为字符串, 默认为代码raise出来的错误, 限制长度200
            result["error_msg"] = result["error_msg"][:200]
        else:
            # 如果error_msg为列表, 默认为逻辑处理错误, 不保存到数据库
            result.pop("error_msg")

        result["complete_path"] = error_file_path

    time_end = perf_counter()

    result["execute_time"] = time_end - time_begin
    record_obj.save_result(**result)


def save_error_message(module, message):
    """
    保存返回的错误信息为excel文件
    :param module:
    :param message:
    :return:
    """
    if isinstance(message, str):
        message = [{"错误信息": message}]
    file_name = (
        f"{module}错误信息" + timezone.now().strftime("%Y%m%dT%H%M%S%f") + ".xlsx"
    )
    error_file_path = os.path.join("error", file_name)
    file_system_storage.mkdir(error_file_path)
    error_file_path = file_system_storage.get_available_name(error_file_path)
    full_path = file_system_storage.path(error_file_path)
    writer = pd.ExcelWriter(full_path)
    df = pd.DataFrame(message)
    df.to_excel(writer, index=False)
    writer.close()

    return full_path


def save_error_message_data(module, message):
    """
    保存返回的错误信息数据为excel文件
    :param module:
    :param message:
    :return:
    """
    file_name = (
        f"{module}错误信息" + timezone.now().strftime("%Y%m%dT%H%M%S%f") + ".xlsx"
    )
    error_file_path = os.path.join("error", file_name)
    file_system_storage.mkdir(error_file_path)
    error_file_path = file_system_storage.get_available_name(error_file_path)
    error_file_path = file_system_storage.path(error_file_path)
    pd.DataFrame(message).to_excel(error_file_path, index=False)
    return error_file_path
