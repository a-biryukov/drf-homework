from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Lesson, Course
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='user@mail.ru', password='123qwe')
        self.moder = User.objects.create(email='moder@mail.ru', password='123qwe')
        moder_group, create = Group.objects.get_or_create(name='moders')
        moder_group.user_set.add(self.moder)
        self.course = Course.objects.create(name='DRF', description='Изучение DRF', owner=self.user)
        self.lesson = Lesson.objects.create(
            name='Тестирование в DRF',
            description='Обучение тестированию',
            course=self.course,
            owner=self.user
        )
        self.lesson_2 = Lesson.objects.create(
            name='Права доступа',
            description='Описание урока',
            course=self.course,
        )

    def test_lesson_retrieve(self):
        """Тестирование просмотра одного урока"""
        url = reverse('lms:lesson_detail', args=(self.lesson.pk,))
        # Неавторизованный пользователь
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Авторизованный пользователь
        self.client.force_authenticate(user=self.user)
        response_1 = self.client.get(url)
        data = response_1.json()
        self.assertEqual(response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('name'), self.lesson.name)
        # Модератор
        self.client.force_authenticate(user=self.moder)
        data = response_1.json()
        self.assertEqual(response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('name'), self.lesson.name)

    def test_lesson_create(self):
        """Тестирование создания урока"""
        url = reverse('lms:lesson_create')
        # Неавторизованный пользователь
        data_1 = {'name': 'Пагинация', 'description': 'https://www.youtube.com/watch?v=bITQ13XCU9Q'}
        response = self.client.get(url, data_1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Авторизованный пользователь
        self.client.force_authenticate(user=self.user)
        response_1 = self.client.post(url, data_1)
        self.assertEqual(response_1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 3)
        # Попытка создания со ссылкой на сторонний ресурс
        data_2 = {'name': 'Пагинация', 'description': 'https://yandex.ru/video/preview/16370055609980825063'}
        response_2 = self.client.post(url, data_2)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Lesson.objects.all().count(), 3)
        # Модератор
        self.client.force_authenticate(user=self.moder)
        response_3 = self.client.post(url, data_1)
        self.assertEqual(response_3.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_update(self):
        """Тестирование обновления урока"""
        url = reverse('lms:lesson_update', args=(self.lesson.pk,))
        # Неавторизованный пользователь
        data_1 = {'name': 'Валидаторы', 'description': 'Инструмент, который проверяет данные, полученные от клиента'}
        response_1 = self.client.patch(url, data_1)
        self.assertEqual(response_1.status_code, status.HTTP_401_UNAUTHORIZED)
        # Авторизованный пользователь
        self.client.force_authenticate(user=self.user)
        response_2 = self.client.patch(url, data_1)
        result = response_2.json()
        self.assertEqual(response_2.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get('name'), 'Валидаторы')
        # Ппытка обновления со ссылкой на сторонний ресурс
        data_2 = {'name': 'Пагинация', 'description': 'https://yandex.ru/video/preview/16370055609980825063'}
        response_3 = self.client.patch(url, data_2)
        self.assertEqual(response_3.status_code, status.HTTP_400_BAD_REQUEST)
        # Модератор
        self.client.force_authenticate(user=self.moder)
        response_2 = self.client.patch(url, data_1)
        result = response_2.json()
        self.assertEqual(response_2.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get('name'), 'Валидаторы')

    def test_lesson_destroy(self):
        """Тестирование удаления урока"""
        url = reverse('lms:lesson_delete', args=(self.lesson.pk,))
        # Неавторизованный пользователь
        response_1 = self.client.delete(url)
        self.assertEqual(response_1.status_code, status.HTTP_401_UNAUTHORIZED)
        # Модератор
        self.client.force_authenticate(user=self.moder)
        response_2 = self.client.delete(url)
        self.assertEqual(response_2.status_code, status.HTTP_403_FORBIDDEN)
        # Авторизованный пользователь
        self.client.force_authenticate(user=self.user)
        response_3 = self.client.delete(url)
        self.assertEqual(response_3.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 1)

    def test_lesson_list(self):
        """Тестирование просмотра списка уроков"""
        url = reverse('lms:lesson_list')
        # Неавторизованный пользователь
        response_1 = self.client.get(url)
        self.assertEqual(response_1.status_code, status.HTTP_401_UNAUTHORIZED)
        # Авторизованный пользователь
        self.client.force_authenticate(user=self.user)
        response_2 = self.client.get(url)
        result_1 = response_2.json()
        data_1 = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': 6,
                    'name': 'Тестирование в DRF',
                    'description': 'Обучение тестированию',
                    'preview': None,
                    'course': 3,
                    'owner': 5
                },
            ]
        }
        self.assertEqual(response_2.status_code, status.HTTP_200_OK)
        self.assertEqual(result_1, data_1)
        # Модератор
        self.client.force_authenticate(user=self.moder)
        response_3 = self.client.get(url)
        result_2 = response_3.json()
        data_2 = {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': 6,
                    'name': 'Тестирование в DRF',
                    'description': 'Обучение тестированию',
                    'preview': None,
                    'course': 3,
                    'owner': 5
                },
                {
                    'id': 7,
                    'name': 'Права доступа',
                    'description': 'Описание урока',
                    'preview': None,
                    'course': 3,
                    'owner': None
                }
            ]
        }
        self.assertEqual(response_3.status_code, status.HTTP_200_OK)
        self.assertEqual(result_2, data_2)
