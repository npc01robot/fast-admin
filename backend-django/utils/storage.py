import io
import os
from datetime import datetime
from typing import IO, Optional, Union

from django.core.files.base import ContentFile, File
from django.core.files.storage import FileSystemStorage as DjangoFileSystemStorage
from django.core.files.storage import default_storage

_FileContent = Union[str, bytes, bytearray, io.BytesIO, IO, ContentFile]


class FileSystemStorage(DjangoFileSystemStorage):
    base_url = "/media/"

    def save(self, name: str, content: _FileContent) -> str:
        if isinstance(content, io.BytesIO):
            content = content.getvalue()
        if isinstance(content, (bytes, bytearray, str)):
            content = ContentFile(content)

        return super().save(name, content)  # type: ignore

    def mkdir(self, name):
        """创建指定路径文件夹"""
        full_path = self.path(name)

        # Create any intermediate directories that do not exist.
        directory = os.path.dirname(full_path)
        if not os.path.exists(directory):
            try:
                if self.directory_permissions_mode is not None:
                    # os.makedirs applies the global umask, so we reset it,
                    # for consistency with file_permissions_mode behavior.
                    old_umask = os.umask(0)
                    try:
                        os.makedirs(directory, self.directory_permissions_mode)
                    finally:
                        os.umask(old_umask)
                else:
                    os.makedirs(directory)
            except FileExistsError:
                # There's a race between os.path.exists() and os.makedirs().
                # If os.makedirs() fails with FileExistsError, the directory
                # was created concurrently.
                pass
        if not os.path.isdir(directory):
            raise IOError("%s exists and is not a directory." % directory)


file_system_storage: FileSystemStorage = default_storage  # type: ignore


def get_full_path(name: str) -> str:
    """获取文件的绝对路径"""
    return file_system_storage.path(name)


def save_temp_file(file_name: str, content: _FileContent):
    """保存临时文件, 自动生成年月日目录"""
    file_name = os.path.join("temp", datetime.now().strftime("%Y%m%d/%H"), file_name)
    return file_system_storage.save(file_name, content)


def save_download_file(file_name: str, content: _FileContent):
    """保存供下载用的文件, 自动生成年月日目录"""
    file_name = os.path.join(
        "download", datetime.now().strftime("%Y%m%d/%H"), file_name
    )
    return file_system_storage.save(file_name, content)


def save_label_file(file_name: str, content: _FileContent):
    """保存物流面单之类的文件, 自动生成年月日目录"""
    from django.conf import settings

    prefix = settings.FILE_LABEL_PREFIX
    file_name = os.path.join(prefix, datetime.now().strftime("%Y%m%d/%H"), file_name)
    return file_system_storage.save(file_name, content)


def save_finance_file(file_name: str, content: _FileContent):
    """保存财务文件, 自动生成年月日目录"""
    from django.conf import settings

    prefix = getattr(settings, "FILE_FINANCE_PREFIX", "finance")
    file_name = os.path.join(prefix, datetime.now().strftime("%Y%m%d/%H"), file_name)
    return file_system_storage.save(file_name, content)
