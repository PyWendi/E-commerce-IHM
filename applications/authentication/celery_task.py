# from celery import shared_task
# from datetime import timedelta
# from .models import Notification
#
# @shared_task
# def delete_expired_notifications():
#     expired_notifications = Notification.objects.filter(created_at__lte=timezone.now() - F('expiration_duration'))
#     expired_notifications.delete()