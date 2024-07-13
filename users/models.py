from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField

from config.settings import NULLABLE
from lms.models import Course, Lesson


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    avatar = models.ImageField(upload_to="users/avatars", verbose_name="Аватар", **NULLABLE, help_text="Загрузите фото")
    phone = models.CharField(max_length=35, verbose_name="Телефон", **NULLABLE, help_text="Введите номер телефона")
    country = CountryField(verbose_name="Страна", help_text="Выберите страну", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payments(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('transfer', 'перевод'),
        ('cash', 'наличные')
    ]

    user = models.ForeignKey(User, verbose_name='Платежи', on_delete=models.CASCADE)
    paid_course = models.ForeignKey(Course, verbose_name='Оплаченный курс', on_delete=models.SET_NULL, **NULLABLE)
    paid_lesson = models.ForeignKey(Lesson, verbose_name='Оплаченный урок', on_delete=models.SET_NULL, **NULLABLE)
    date_of_payment = models.DateField(verbose_name='Дата оплаты')
    payment_amount = models.IntegerField(verbose_name='Сумма оплаты')
    payment_method = models.CharField(max_length=50, verbose_name='Способ оплаты', choices=PAYMENT_METHOD_CHOICES)

    class Meta:
        verbose_name = "Платежи"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return (f'Дата платежа: {self.date_of_payment}'
                f'Сумма: {self.payment_amount}, способ оплаты: {self.payment_method}'
                f'Курс: {self.paid_course}' if self.paid_course else f'Урок: {self.paid_lesson}'
                f'Пользователь: {self.user.email}')
