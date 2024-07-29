from django.contrib.auth.models import AbstractUser
from django.db import models

from config.settings import NULLABLE
from lms.models import Course, Lesson


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    avatar = models.ImageField(upload_to="users/avatars", verbose_name='Аватар', **NULLABLE, help_text='Загрузите фото')
    phone = models.CharField(max_length=35, verbose_name='Телефон', **NULLABLE, help_text='Введите номер телефона')
    country = models.CharField(max_length=100, verbose_name='Страна', help_text='Введите страну', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class Payments(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('transfer', 'перевод'),
        ('cash', 'наличные')
    ]

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.SET_NULL,
        **NULLABLE,
        help_text='Укажите пользователя'
    )
    course = models.ForeignKey(
        Course,
        verbose_name='Оплаченный курс',
        on_delete=models.SET_NULL, **NULLABLE,
        help_text='Укажите оплаченный курс'
    )
    lesson = models.ForeignKey(
        Lesson, verbose_name='Оплаченный урок',
        on_delete=models.SET_NULL, **NULLABLE,
        help_text='Укажите оплаченный урок'
    )
    paid_at = models.DateField(verbose_name='Дата оплаты',  **NULLABLE, help_text='Укажите дату оплаты')
    amount = models.PositiveIntegerField(verbose_name='Сумма оплаты', help_text='Укажите сумму оплаты')
    method = models.CharField(
        max_length=50,
        verbose_name='Способ оплаты',
        choices=PAYMENT_METHOD_CHOICES,
        **NULLABLE,
        help_text='Выберите способ оплаты'
    )
    link = models.URLField(
        max_length=400,
        verbose_name='Ccылка на оплату',
        **NULLABLE,
        help_text='Укажите ссылку на оплату'
    )
    session_id = models.CharField(
        max_length=255,
        verbose_name='ID сессии',
        **NULLABLE,
        help_text='Укажите ID сессии'
    )

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return (f'Дата платежа: {self.paid_at}'
                f'Сумма: {self.amount}, способ оплаты: {self.method}'
                f'Курс: {self.course}' if self.course else f'Урок: {self.lesson}'
                f'Пользователь: {self.user}')


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', **NULLABLE)

    def __str__(self):
        return f'{self.user, self.course}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
