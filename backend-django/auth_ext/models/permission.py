from django.db import models


class Permission(models.Model):
    MENU_TYPE = 0
    IFRAME_TYPE = 1
    URL_TYPE = 2
    PERMISSION_TYPE_CHOICES = (
        (MENU_TYPE, "Menu"),
        (IFRAME_TYPE, "Iframe"),
        (URL_TYPE, "Url"),
    )

    id = models.AutoField(primary_key=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    menu_type = models.IntegerField(choices=PERMISSION_TYPE_CHOICES, default=MENU_TYPE)
    title = models.CharField(max_length=255)

    class Meta:
        db_table = "permission"
        verbose_name = "Permission"
        managed = True
