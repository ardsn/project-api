from app.models import AvailableDay, Business, Professional, City
from datetime import datetime, timedelta, time
from unittest.mock import patch
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class TestAvailableDayView(APITestCase):

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

        cls.professional = Professional.objects.create(
            name="John Doe",
            email="email@example.com",
            phone="11 99595-4250",
            business=cls.business,
            cpf="111.444.777-35",
            speciality="Dentista",
            schedule={
                "0": {
                    "start": "08:00",
                    "end": "17:00",
                    "breaks": []
                }
            }
        )

        cls.mock_datetime = datetime(2025, 1, 1, 10, 0, 0)
        
        cls.available_day_args = {
            "business": cls.business,
            "professional": cls.professional,
            "date": cls.mock_datetime.date()
        }
        
    def setUp(self):
        self.client.force_authenticate(user=self.user)

    @patch('app.validators.datetime')
    def test_list_available_days(self, mock_datetime):
        mock_datetime.now.return_value = self.mock_datetime
        _ = AvailableDay.objects.create(**self.available_day_args)

        response = self.client.get(reverse('availableday-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_list_available_days_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('availableday-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('app.validators.datetime')
    def test_get_available_day(self, mock_datetime):
        mock_datetime.now.return_value = self.mock_datetime
        available_day = AvailableDay.objects.create(**self.available_day_args)
        response = self.client.get(
            reverse('availableday-detail', args=[available_day.id])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], available_day.id)

    @patch('app.validators.datetime')
    def test_get_available_day_unauthenticated(self, mock_datetime):
        mock_datetime.now.return_value = self.mock_datetime
        self.client.force_authenticate(user=None)
        available_day = AvailableDay.objects.create(**self.available_day_args)
        response = self.client.get(
            reverse('availableday-detail', args=[available_day.id])
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('app.validators.datetime')
    def test_create_available_day(self, mock_datetime):
        mock_datetime.now.return_value = self.mock_datetime
        available_day_data = {
            "business": self.business.id,
            "professional": self.professional.id,
            "date": self.available_day_args["date"].strftime("%Y-%m-%d")
        }

        response = self.client.post(
            reverse('availableday-list'),
            available_day_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AvailableDay.objects.count(), 1)

    def test_create_available_day_unauthenticated(self):
        self.client.force_authenticate(user=None)
        available_day_data = {
            "business": self.business.id,
            "professional": self.professional.id,
            "date": self.available_day_args["date"].strftime("%Y-%m-%d")
        }

        response = self.client.post(
            reverse('availableday-list'),
            available_day_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('app.validators.datetime')
    def test_create_available_day_with_invalid_field(self, mock_datetime):
        mock_datetime.now.return_value = self.mock_datetime
        available_day_data = {
            "business": self.business.id,
            "professional": self.professional.id,
            "date": self.mock_datetime.date() - timedelta(days=1)
        }

        response = self.client.post(
            reverse('availableday-list'),
            available_day_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('app.validators.datetime')
    def test_refuse_duplicate_available_day(self, mock_datetime):
        mock_datetime.now.return_value = self.mock_datetime
        available_day_data = {
            "business": self.business.id,
            "professional": self.professional.id,
            "date": self.available_day_args["date"].strftime("%Y-%m-%d")
        }

        response = self.client.post(
            reverse('availableday-list'),
            available_day_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(
            reverse('availableday-list'),
            available_day_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('app.validators.datetime')
    def test_update_available_day_field(self, mock_datetime):
        mock_datetime.now.return_value = self.mock_datetime
        available_day = AvailableDay.objects.create(**self.available_day_args)
        updated_fields = {
            "blocked_start_time": "10:00",
            "blocked_end_time": "11:00"
        }

        response = self.client.patch(
            reverse('availableday-detail', args=[available_day.id]),
            updated_fields,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(AvailableDay.objects.count(), 1)
        self.assertEqual(
            AvailableDay.objects.get(id=available_day.id).blocked_start_time,
            time.fromisoformat(updated_fields["blocked_start_time"])
        )
        self.assertEqual(
            AvailableDay.objects.get(id=available_day.id).blocked_end_time,
            time.fromisoformat(updated_fields["blocked_end_time"])
        )
    
    @patch('app.validators.datetime')
    def test_update_available_day_field_unauthenticated(self, mock_datetime):
        mock_datetime.now.return_value = self.mock_datetime
        self.client.force_authenticate(user=None)
        available_day = AvailableDay.objects.create(**self.available_day_args)
        updated_fields = {
            "blocked_start_time": "10:00",
            "blocked_end_time": "11:00"
        }

        response = self.client.patch(
            reverse('availableday-detail', args=[available_day.id]),
            updated_fields,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('app.validators.datetime')
    def test_delete_available_day(self, mock_datetime):
        mock_datetime.now.return_value = self.mock_datetime
        available_day = AvailableDay.objects.create(**self.available_day_args)

        response = self.client.delete(
            reverse('availableday-detail', args=[available_day.id])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(AvailableDay.objects.count(), 0)

    @patch('app.validators.datetime')
    def test_delete_available_day_unauthenticated(self, mock_datetime):
        mock_datetime.now.return_value = self.mock_datetime
        self.client.force_authenticate(user=None)
        available_day = AvailableDay.objects.create(**self.available_day_args)

        response = self.client.delete(
            reverse('availableday-detail', args=[available_day.id])
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)