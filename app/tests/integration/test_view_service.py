from app.models import Business, City, Service
from app.utils import timedelta_to_string
from datetime import timedelta
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

class TestServiceView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        cls.city = City.objects.get(name="Ariquemes", state="RO")

        cls.business = Business.objects.create(
            name="Clínica Fagundes",
            category="C1",
            city=cls.city,
            address="Rua 1",
            public_phone="(12) 3456-7890",
            restricted_phone="(12) 3456-7890",
            email="clinica@fagundes.com",
            schedule={
                "0": {
                    "start": "08:00",
                    "end": "17:00",
                    "breaks": []
                }
            },
            closed_on_holidays=False
        )

        cls.service_args = {
            "name": "Test Service",
            "description": "Test Description",
            "price": 100.00,
            "duration": timedelta(minutes=30),
            "business": cls.business
        }
        
    def setUp(self):
        self.client.force_authenticate(user=self.user)

    def test_list_services(self):
        _ = Service.objects.create(**self.service_args)

        response = self.client.get(reverse('service-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_list_services_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('service-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_service(self):
        service = Service.objects.create(**self.service_args)
        response = self.client.get(
            reverse('service-detail', args=[service.id])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], service.id)

    def test_get_service_unauthenticated(self):
        self.client.force_authenticate(user=None)
        service = Service.objects.create(**self.service_args)
        response = self.client.get(
            reverse('service-detail', args=[service.id])
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_service(self):
        service_data = (
            self.service_args
            |
            {
                "business": self.business.id,
                "duration": timedelta_to_string(self.service_args["duration"])
            }
        )

        response = self.client.post(
            reverse('service-list'),
            service_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Service.objects.count(), 1)

    def test_create_service_unauthenticated(self):
        self.client.force_authenticate(user=None)
        service_data = (
            self.service_args
            |
            {
                "business": self.business.id,
                "duration": timedelta_to_string(self.service_args["duration"])
            }
        )

        response = self.client.post(
            reverse('service-list'),
            service_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_service_with_invalid_field(self):
        service_data = (
            self.service_args
            |
            {
                "business": self.business.id,
                "price": -50.00
            }
        )

        response = self.client.post(
            reverse('service-list'),
            service_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_refuse_duplicate_service(self):
        service_data = (
            self.service_args
            |
            {
                "business": self.business.id,
                "duration": timedelta_to_string(self.service_args["duration"])
            }
        )
        response = self.client.post(
            reverse('service-list'),
            service_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        other_service_data = (
            self.service_args
            |
            {
                "business": self.business.id,
                "duration": "01:30"
            }
        )
        response = self.client.post(
            reverse('service-list'),
            other_service_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_service_field(self):
        service = Service.objects.create(**self.service_args)
        updated_field = {"description": "Test description updated"}

        response = self.client.patch(
            reverse('service-detail', args=[service.id]),
            updated_field,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Service.objects.count(), 1)
        self.assertEqual(Service.objects.get(id=service.id).description, updated_field["description"])

    def test_update_service_field_unauthenticated(self):
        self.client.force_authenticate(user=None)
        service = Service.objects.create(**self.service_args)
        updated_field = {"description": "Test description updated"}

        response = self.client.patch(
            reverse('service-detail', args=[service.id]),
            updated_field,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_service(self):
        service = Service.objects.create(**self.service_args)
        response = self.client.delete(
            reverse('service-detail', args=[service.id])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Service.objects.count(), 0)

    def test_delete_service_unauthenticated(self):
        self.client.force_authenticate(user=None)
        service = Service.objects.create(**self.service_args)

        response = self.client.delete(
            reverse('service-detail', args=[service.id])
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        