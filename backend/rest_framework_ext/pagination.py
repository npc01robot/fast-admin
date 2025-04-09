import math
from collections import OrderedDict
from urllib import parse

from rest_framework.pagination import CursorPagination, PageNumberPagination
from rest_framework.response import Response


class PageNumberPaginationExt(PageNumberPagination):
    page_size_query_param = "page_size"

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("page", self.page.number),
                    ("page_size", self.page.paginator.per_page),
                    (
                        "page_count",
                        math.ceil(
                            self.page.paginator.count / self.page.paginator.per_page
                        ),
                    ),
                    ("total", self.page.paginator.count),
                    # ('next', self.get_next_link()),
                    # ('previous', self.get_previous_link()),
                    ("list", data),
                ]
            )
        )


class FormatPageNumberPaginationExt(PageNumberPagination):
    page_size_query_param = "page_size"

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("code", 0),
                    ("message", "success"),
                    ("count", self.page.paginator.count),
                    ("page", self.page.number),
                    ("page_size", self.page.paginator.per_page),
                    ("data", data),
                ]
            )
        )


class CursorPaginationExt(CursorPagination):
    # 默认一页的条数
    page_size = 10

    # 用户可以自定义选择一页的条数，但最多显示max_page_size设置的条数
    page_size_query_param = "page_size"
    max_page_size = 1000

    def get_paginated_response(self, data):
        next = self.get_next_link()
        previous = self.get_previous_link()
        # 获取 cursor给前端
        pre_cursor = self.get_cursor(previous)
        next_cursor = self.get_cursor(next)
        return Response(
            OrderedDict(
                [
                    ("next", next),
                    ("previous", previous),
                    ("pre_cursor", pre_cursor),
                    ("next_cursor", next_cursor),
                    ("results", data),
                ]
            )
        )

    @staticmethod
    def get_cursor(url):
        if url:
            query_dict = parse.parse_qs(parse.urlparse(url).query)
            return query_dict.get("cursor", [""])[0]
        else:
            return ""
