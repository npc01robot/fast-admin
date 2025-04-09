import base64
from io import BytesIO

import pandas as pd

from basic.models import Basic
from generics.models import ImportExportRecord
from generics.tasks import upload_handle_task, upload_handler


@upload_handler(module=ImportExportRecord.BASIC_UPLOAD)
def upload_basic_upload(file, basic_type):
    base64_str = file.split(",")[1]

    # 将 Base64 字符串解码为字节流
    file_bytes = base64.b64decode(base64_str)
    bio = BytesIO(file_bytes)
    df = pd.read_excel(bio)
    df.columns = ["id", "name", "parent_id", "sort", "remark"]
    df["parent_id"] = df["parent_id"].fillna(-1).astype(int)
    list_data = df.to_dict(orient="records")
    group_data = {}
    for data in list_data:
        # 处理父级编号 为空的情况
        try:
            if data["parent_id"] == -1 and data.get("id") not in group_data.keys():
                basic = Basic.objects.create(
                    name=data.get("name"),
                    parent_id=None,
                    sort=data.get("sort"),
                    remark=data.get("remark"),
                    type=basic_type,
                )
                group_data[data.get("id")] = basic
            elif data["parent_id"] in group_data.keys():
                basic = Basic.objects.create(
                    name=data.get("name"),
                    parent_id=group_data.get(data.get("parent_id")).id,
                    sort=data.get("sort"),
                    remark=data.get("remark"),
                    type=basic_type,
                )
                group_data[data.get("id")] = basic
        except Exception as e:
            continue
    return {"status": ImportExportRecord.STATUS_COMPLETE, "message": "导入成功"}
