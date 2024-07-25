from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course
from users.models import User, Subscription


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='user@mail.ru', password='123qwe')
        self.course = Course.objects.create(name='DRF', description='Изучение DRF')
        self.url = reverse('users:user_subscription')

    def test_subscription(self):
        """Тестирование создания и удаления подписки"""
        data = {'user': self.user.id, 'course': self.course.id}
        # Неавторизованный пользователь
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Добавление подписки
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.all().count(), 1)
        # Удаление подписки
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.all().count(), 0)
