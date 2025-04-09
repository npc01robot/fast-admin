from celery import shared_task

from auth_ext.models.media import FileMedia


@shared_task
def export_data():
    FileMedia()
