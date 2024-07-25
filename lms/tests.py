from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Lesson, Course
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='user@mail.ru', password='123qwe')
        self.course = Course.objects.create(name='DRF', description='Изучение DRF', owner=self.user)
        self.lesson = Lesson.objects.create(
            name='Тестирование в DRF',
            description='Обучение тестированию',
            course=self.course,
            owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse('lms:lesson_detail', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('name'), self.lesson.name)

    def test_lesson_create(self):
        url = reverse('lms:lesson_create')

        data_1 = {'name': 'Пагинация', 'description': 'https://www.youtube.com/watch?v=bITQ13XCU9Q'}
        response_1 = self.client.post(url, data_1)
        self.assertEqual(response_1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

        data_2 = {'name': 'Пагинация', 'description': 'https://yandex.ru/video/preview/16370055609980825063'}
        response_2 = self.client.post(url, data_2)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse('lms:lesson_update', args=(self.lesson.pk,))

        data = {'name': 'Валидаторы', 'description': 'Инструмент, который проверяет данные, полученные от клиента'}
        response_1 = self.client.patch(url, data)
        result = response_1.json()
        self.assertEqual(response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get('name'), 'Валидаторы')

        data_2 = {'name': 'Пагинация', 'description': 'https://yandex.ru/video/preview/16370055609980825063'}
        response_2 = self.client.patch(url, data_2)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_lesson_destroy(self):
        url = reverse('lms:lesson_delete', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse('lms:lesson_list')

        response = self.client.get(url)
        result = response.json()
        data = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': 4,
                    'name': 'Тестирование в DRF',
                    'description': 'Обучение тестированию',
                    'preview': None,
                    'course': 3,
                    'owner': 3
                },
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result, data)
