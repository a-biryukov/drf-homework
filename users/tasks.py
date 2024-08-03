from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from users.models import Subscription, User


@shared_task
def sending_mails_to_subscribers(course):
    """
    Отправка писем подписчикам при обновлении курса
    :param course: объект модели Course
    """
    subscriptions = Subscription.objects.filter(course=course.id)
    subscribers_emails = [subscription.user for subscription in subscriptions]

    send_mail(
        'Обновление курса',
        f'Курс {course} обновлен',
        EMAIL_HOST_USER,
        subscribers_emails)


@shared_task
def check_last_login():
    """Блокирует пользователей, которые не заходили больше 30 дней"""
    month_ago = timezone.now().today() - timedelta(days=30)
    if User.objects.filter(last_login__lte=month_ago, is_active=True).exists():
        users_didnt_login = User.objects.filter(last_login__lte=month_ago, is_active=True)

        for user in users_didnt_login:
            user.is_active = False
            user.save()
