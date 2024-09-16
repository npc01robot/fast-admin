from django.db import models

from auth_ext.models import AuthExtUser


class FileMedia(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AuthExtUser, null=True, related_name='files', on_delete=models.CASCADE)
    path = models.FileField(upload_to='media/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "file_media"
        managed = True
