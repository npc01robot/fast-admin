from django.urls import re_path

from generics.views import ImportExportRecordView, ImportExportTypeView, UploadFileView

# 对外担保
urlpatterns = [
    re_path(r"^export/$", ImportExportRecordView.as_view(), name="export"),
    re_path(r"^export_type/$", ImportExportTypeView.as_view(), name="import"),
    re_path(r"upload/$", UploadFileView.as_view(), name="upload"),
]
