import os
import zipfile
from collections import OrderedDict
from datetime import datetime
from io import BytesIO
from typing import List, Optional

import pandas as pd
import xlsxwriter
from django.shortcuts import HttpResponse
from django.utils import timezone

from utils.storage import file_system_storage


def export(data):
    """
    :param data: header_map: 主表信息, key为字段名, value为中文名
                detail_header_map: 从表信息, key为字段名, value为中文名
                detail: 主表中从表数据名
                data_list: 主从表数据, 为序列化后的数据list
    :return: BytesIO文件流
    pandas
    pf = pd.DataFrame(data_list)
    pf = pf[header]
    pf.rename(columns=header_map, inplace=True)
    pf.fillna('', inplace=True)
    writer = pd.ExcelWriter(bio, engine="xlsxwriter")
    pf.to_excel(writer, encoding='utf-8', index=False)
    writer.close()
    bio.seek(0)
    """
    try:
        header_map = data.get("header_map", {})
        head_field_str_list = data.get(
            "head_field_str", []
        )  # 指定头部字段哪些以字符串格式输出防止科学计数
        detail_header_map = data.get("detail_header_map", {})
        data_list = data.get("data_list", [])
        detail = data.get("detail", "")
        bio = BytesIO()
        book = xlsxwriter.Workbook(bio)
        sheet1 = book.add_worksheet("数据列表")
        header = header_map.values()
        header_values = list(header_map.keys())
        header_detail = detail_header_map.values()
        header_values_detail = list(detail_header_map.keys())
        sheet1.write_row(0, 0, header)
        if detail:
            sheet2 = book.add_worksheet("详细信息")
            sheet2.write_row(0, 0, header_detail)
        bg_format = book.add_format({"bg_color": "CBD3D5"})  # 灰色
        bg_format_button = book.add_format({"font_color": "2EB3F5"})  # 蓝色
        row = 1
        len_detail = 1
        len_header = len(header)
        flag = False
        from utils import time_format_local

        for data in data_list:
            for i, index in enumerate(header):
                _field = header_values[i]
                value = data.get(_field)
                if str(_field).endswith("_time") and isinstance(
                    value, (datetime, pd.Timestamp)
                ):
                    if isinstance(value, pd.Timestamp):
                        value = value.to_pydatetime()
                    value = time_format_local(value)
                value = str(value) if _field in head_field_str_list else value
                sheet1.write(row, i, value)

            # 填写sheet2从表信息
            if detail:
                detail_list = data.pop(detail, [])
                if detail_list:
                    sheet1.write_formula(
                        row,
                        len_header,
                        f'=HYPERLINK("#详细信息!A{len_detail + 1}","查看详情")',
                        bg_format_button,
                    )
                for detail_data in detail_list:
                    for i, index in enumerate(header_detail):
                        detail_field = header_values_detail[i]
                        detail_value = detail_data.get(detail_field)
                        if str(detail_field).endswith("_time") and isinstance(
                            detail_value, datetime
                        ):
                            detail_value = time_format_local(detail_value)
                        try:
                            if flag:
                                sheet2.write(len_detail, i, detail_value, bg_format)
                            else:
                                sheet2.write(len_detail, i, detail_value)
                        except:
                            sheet2.write(len_detail, i, str(detail_value))
                    len_detail += 1
                flag = ~flag

            row += 1
        book.close()
        bio.seek(0)
        return {"status": True, "data": bio}
    except Exception as e:
        return {"status": False, "msg": e}


def export_excel_data(data, field_header_map=None):
    """
    data : 序列化后的方法, 格式为列表嵌套字典
    field_header_map: 字段 和 excel 表头的映射
    """

    import pandas as pd

    bio = BytesIO()
    df = pd.DataFrame(data)
    if field_header_map and isinstance(field_header_map, OrderedDict):
        df = df[field_header_map.keys()]
        df.columns = field_header_map.values()
    writer = pd.ExcelWriter(bio, engine="xlsxwriter")
    df.to_excel(writer, index=False)
    writer.close()
    bio.seek(0)  # 方便调用方读写
    return bio


def export_template(name, header: List[str], content: Optional[str] = None):
    """
    生成excel模板
    :param name: Sheet名称
    :param header: 表头
    :param content: 模板备注
    """
    try:
        bio = BytesIO()
        book = xlsxwriter.Workbook(bio)
        sheet = book.add_worksheet(name)
        sheet.write_row(0, 0, header)
        sheet.freeze_panes(1, 0)
        if isinstance(content, bytes):
            content = content.decode("utf-8", errors="ignore")
        if content:
            # 模板增加注解
            sheet.insert_textbox(
                10,
                0,
                content,
                {
                    "width": 500,
                    "height": 100,
                    "font": {"color": "red"},
                },
            )
        book.close()
        bio.seek(0)
        return {"status": True, "data": bio}
    except Exception as e:
        return {"status": False, "msg": e}


def pds_export_by_sql(file_name, sql, params=None, date_local_columns=None):
    """
    通过传入sql导出文件
    :param file_name:
    :param sql:
    :return:
    """

    from django.conf import settings
    from django.db import connection

    outfile = BytesIO()
    df = pd.read_sql(sql, connection, params=params)
    if date_local_columns:
        # 把utc时间转换为本地显示,execl导出时不支持带时区把时间格式转化为str
        for col in date_local_columns:
            df[col] = df[col].astype("datetime64[ns]")
            df[col] = (
                df[col]
                .dt.tz_localize(settings.TIME_ZONE)
                .dt.tz_convert(settings.CN_TIME_ZONE)
                .astype("str")
            )
            df.loc[df[col] == "NaT", col] = ""
    df.to_excel(outfile, index=False)
    binary_data = outfile.getvalue()
    return binary_data


def import_excel(file):
    excel_raw_data = pd.read_excel(file, dtype={"跟踪单号": str})
    return list(excel_raw_data.values)


def merge_cells(
    data,
    merge_fields: list,
    field_index: list = None,
    header: list = None,
    file_path: str = "",
):
    """
    根据传入的merge_fields从左到右的优先级生成excel文件, 并将相同的数据合并
    :param data: 可以转化为DataFrame格式的数据, eg: [{},{}...], [[],[],...]
    :param merge_fields: 需要合并的字段
    :param field_index: 字段排列的顺序
    :param header: excel文件表头
    :param file_path: 文件保存路径
    :return: bio data
    """
    df = pd.DataFrame(data)
    bio = merge_cells_by_data_frame(df, merge_fields, field_index, header)
    if file_path:
        with open(file_path, "wb") as w:
            w.write(bio.read())
    return bio


def merge_cells_by_data_frame(data_frame, merge_fields, field_index=None, header=None):
    """
    根据传入的merge_fields从左到右的优先级合并值相同的单元格
    :param data_frame:
    :param merge_fields:需要合并的字段
    :param field_index: 字段排列的顺序
    :param header: excel文件表头
    :return: excel2007文件数据
    """

    self_copy = pd.DataFrame(data_frame, copy=True, columns=field_index)
    self_copy.fillna("", inplace=True)
    cols = list(self_copy.columns.values)

    assert len(cols) == len(set(cols)), "数据字段不允许重复"
    # 校验key_cols中各元素 是否都包含与对象的列
    assert not set(merge_fields) - set(
        cols
    ), f"merge_fields error: {set(merge_fields) - set(cols)}"
    assert not all(
        v in ("_rank", "_for_group", "_count") for v in cols
    ), "_rank, _for_group, _count为辅助字段,请勿重复"

    bio = BytesIO()
    wb2007 = xlsxwriter.Workbook(bio)
    worksheet2007 = wb2007.add_worksheet()
    # 格式
    format_top = wb2007.add_format({"border": 1, "bold": True, "text_wrap": True})
    format_other = wb2007.add_format({"border": 1, "valign": "vcenter"})
    # 写表头
    for i, value in enumerate(header or cols):
        worksheet2007.write(0, i, value, format_top)

    # 额外插入一列用于分组, 防止出现所有列都需要合并的情况下报错
    self_copy["_for_group"] = self_copy.iloc[:, -1:]

    all_fields_col = {v: k for k, v in enumerate(cols)}
    # 处理需要合并的单元格
    for merge_index, field in enumerate(merge_fields):
        rank_index = merge_fields[: merge_index + 1]
        # 设置辅助列
        self_copy["key_cols"] = self_copy[rank_index[0]].factorize()[0]
        # 记录重复顺序
        self_copy["_rank"] = (
            self_copy.groupby(rank_index, as_index=False)
            .rank(method="first")
            .loc[:, "key_cols"]
        )
        # 记录重复次数
        self_copy["_count"] = (
            self_copy.groupby(rank_index, as_index=False)
            .rank(method="max")
            .loc[:, "key_cols"]
        )

        col = self_copy[field]
        field_col = all_fields_col.pop(field)
        for cell_index, cell in enumerate(col):
            if self_copy.loc[cell_index, "_count"] == 1:
                # 计数为一个不需要合并单元格
                worksheet2007.write(
                    cell_index + 1,
                    field_col,
                    self_copy.iloc[cell_index, field_col],
                    format_other,
                )
                continue

            if self_copy.loc[cell_index, "_rank"] == 1:
                # 合并单元格，根据_count列判断需要合并几个
                worksheet2007.merge_range(
                    cell_index + 1,
                    field_col,
                    cell_index + int(self_copy.loc[cell_index, "_count"]),
                    field_col,
                    self_copy.iloc[cell_index, field_col],
                    format_other,
                )
    # 处理不需要合并的单元格
    for field, field_col in all_fields_col.items():
        col = self_copy[field]
        for cell_index, cell in enumerate(col):
            worksheet2007.write(
                cell_index + 1,
                field_col,
                self_copy.iloc[cell_index, field_col],
                format_other,
            )

    wb2007.close()
    bio.seek(0)
    return bio


def generate_filepath(prefix, module, suffix=".xlsx"):
    filename = f"{prefix}%d%s" % (timezone.now().timestamp(), suffix)
    filepath = os.path.join(
        "download", str(module), timezone.now().strftime("%Y%m%d"), filename
    )
    file_system_storage.mkdir(filepath)
    file_path = file_system_storage.get_available_name(filepath)
    file_path = file_system_storage.path(file_path)
    return file_path


def zip_folder(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                zipf.write(
                    os.path.join(root, file),
                    os.path.relpath(os.path.join(root, file), folder_path),
                )
