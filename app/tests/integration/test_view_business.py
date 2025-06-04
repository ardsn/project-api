from app.models import Business, City
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

class TestBusinessView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        cls.business_args = {
            "name": "Clínica Fagundes",
            "category": "C1",
            "city": City.objects.get(name="Ariquemes", state="RO"),
            "address": "Rua 1",
            "public_phone": "(12) 3456-7890",
            "restricted_phone": "(12) 3456-7890",
            "email": "clinica@fagundes.com",
            "schedule": {
                "0": {
                    "start": "08:00",
                    "end": "17:00",
                    "breaks": []
                }
            },
            "closed_on_holidays": False
        }

    def setUp(self):
        self.client.force_authenticate(user=self.user)

    def test_list_businesses(self):
        _ = Business.objects.create(**self.business_args)

        response = self.client.get(reverse('business-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_list_businesses_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('business-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_business(self):
        business = Business.objects.create(**self.business_args)
        response = self.client.get(
            reverse('business-detail', args=[business.id])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], business.id)

    def test_get_business_unauthenticated(self):
        self.client.force_authenticate(user=None)
        business = Business.objects.create(**self.business_args)
        response = self.client.get(
            reverse('business-detail', args=[business.id])
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_business(self):
        business_data = self.business_args.copy()
        business_data |= {"city": 1}
        response = self.client.post(
            reverse('business-list'),
            business_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Business.objects.count(), 1)

    def test_create_business_unauthenticated(self):
        business_data = self.business_args.copy()
        business_data |= {"city": 1}
        self.client.force_authenticate(user=None)

        response = self.client.post(
            reverse('business-list'),
            business_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_business_with_invalid_field(self):
        business_data = self.business_args.copy()
        business_data |= {"city": 1, "public_phone": "3456-7890"}

        response = self.client.post(
            reverse('business-list'),
            business_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_business_field(self):
        business = Business.objects.create(**self.business_args)
        updated_field = {"name": "Clínica Fagundes 2"}

        response = self.client.patch(
            reverse('business-detail', args=[business.id]),
            updated_field,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Business.objects.count(), 1)
        self.assertEqual(Business.objects.get(id=business.id).name, updated_field["name"])

    def test_update_business_field_unauthenticated(self):
        self.client.force_authenticate(user=None)
        business = Business.objects.create(**self.business_args)
        updated_field = {"name": "Clínica Fagundes 2"}

        response = self.client.patch(
            reverse('business-detail', args=[business.id]),
            updated_field,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_business(self):
        business = Business.objects.create(**self.business_args)
        response = self.client.delete(
            reverse('business-detail', args=[business.id])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Business.objects.count(), 0)

    def test_delete_business_unauthenticated(self):
        self.client.force_authenticate(user=None)
        business = Business.objects.create(**self.business_args)

        response = self.client.delete(
            reverse('business-detail', args=[business.id])
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)