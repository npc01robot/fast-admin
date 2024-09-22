import base64
import io
import os
import re
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


def save_upload_file(file_name: str, content: _FileContent):
    """保存上传文件, 自动生成年月日目录"""
    file_name = os.path.join("upload", datetime.now().strftime("%Y%m%d/%H"), file_name)
    return file_system_storage.save(file_name, content)


def base64_to_file(base64_data: str, file_name: str):
    """base64字符串转文件"""
    match = re.match(r"data:(?P<type>[^;]+);base64,(?P<data>.*)", base64_data)
    if not match:
        raise ValueError("Invalid Base64 data format")

    file_type = match.group("type")  # 获取文件类型
    file_data = match.group("data")  # 获取实际的 Base64 数据

    # 解码 Base64 数据
    decoded_file_data = base64.b64decode(file_data)
    file_name = (
        "uploaded_file" if not file_name else file_name + "." + file_type.split("/")[-1]
    )

    # 创建 ContentFile
    content_file = ContentFile(decoded_file_data, name=file_name)
    return content_file, file_type, file_name


def save_upload_base64_file(base64_data: str, file_name: str = None):
    """保存上传的base64文件, 自动生成年月日目录"""
    content_file, file_type, file_name = base64_to_file(base64_data, file_name)
    return save_upload_file(file_name, content_file)
