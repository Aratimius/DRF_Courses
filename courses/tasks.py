from celery import shared_task
from config.settings import EMAIL_HOST_USER
from django.core.mail import send_mail


@shared_task
def send_notification(email, message):
    """Отправляет пользователю уведомление о обновлении курса"""
    send_mail('Уведомление об обновлении курса', message, EMAIL_HOST_USER, [email])
