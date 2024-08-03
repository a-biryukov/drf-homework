from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from users.models import Subscription


@shared_task
def sending_mails_to_subscribers(course):
    """
    Отправка писем подписчикам
    :param course: объект модели Course
    """
    subscriptions = Subscription.objects.filter(course=course.id)
    subscribers_emails = [subscription.user for subscription in subscriptions]

    send_mail(
        'Обновление курса',
        f'Курс {course} обновлен',
        EMAIL_HOST_USER,
        subscribers_emails)
