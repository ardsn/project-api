from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class TestCityView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_list_cities(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('city-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_list_cities_unauthenticated(self):
        response = self.client.get(reverse('city-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
