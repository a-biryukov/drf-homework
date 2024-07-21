from django.db import models

from config.settings import NULLABLE, AUTH_USER_MODEL


class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название курса')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    preview = models.ImageField(verbose_name='Превью', **NULLABLE)
    owner = models.ForeignKey(AUTH_USER_MODEL, verbose_name='Владелец', on_delete=models.SET_NULL, **NULLABLE)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название урока')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    preview = models.ImageField(verbose_name='Превью', **NULLABLE)
    course = models.ForeignKey(Course, verbose_name='Курс', on_delete=models.SET_NULL, **NULLABLE)
    owner = models.ForeignKey(AUTH_USER_MODEL, verbose_name='Владелец', on_delete=models.SET_NULL, **NULLABLE)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.name
