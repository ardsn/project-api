from app.models import (
    Appointment,
    Business,
    Professional,
    City,
    Customer,
    Service
)
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from unittest.mock import patch
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

class TestAppointmentView(APITestCase):

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

        cls.customer = Customer.objects.create(
            business=cls.business,
            name="Test Customer",
            registration_source="WEBSITE",
            cpf="111.444.777-35",
            email="test@example.com",
            phone="11995954250"
        )

        cls.service = Service.objects.create(
            name="Test Service",
            description="Test Description",
            price=100.00,
            duration=timedelta(minutes=30),
            business=cls.business
        )
        cls.mock_datetime = datetime.now(ZoneInfo("America/Sao_Paulo"))

        cls.appointment_args = {
            "business": cls.business,
            "customer": cls.customer,
            "service": cls.service,
            "professional": cls.professional,
            "datetime": cls.mock_datetime + timedelta(hours=3),
            "source": "WHATSAPP"
        }
    
    def setUp(self):
        self.client.force_authenticate(user=self.user)

    @patch('app.validators.datetime')
    def test_list_appointments(self, mock_datetime):
        mock_datetime.now.return_value = self.mock_datetime
        _ = Appointment.objects.create(**self.appointment_args)

        response = self.client.get(reverse('appointment-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_list_appointments_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('appointment-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('app.validators.datetime')
    def test_get_appointment(self, mock_datetime):
        mock_datetime.now.return_value = self.mock_datetime
        appointment = Appointment.objects.create(**self.appointment_args)

        response = self.client.get(
            reverse('appointment-detail', args=[appointment.id])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], appointment.id)

    @patch('app.validators.datetime')
    def test_get_appointment_unauthenticated(self, mock_datetime):
        mock_datetime.now.return_value = self.mock_datetime
        self.client.force_authenticate(user=None)
        appointment = Appointment.objects.create(**self.appointment_args)

        response = self.client.get(
            reverse('appointment-detail', args=[appointment.id])
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('app.validators.datetime')
    def test_create_appointment(self, mock_datetime):
        mock_datetime.now.return_value = self.mock_datetime
        appointment_data = (
            self.appointment_args
            |
            {
                "business": self.business.id,
                "customer": self.customer.id,
                "service": self.service.id,
                "professional": self.professional.id,
                "datetime": self.appointment_args["datetime"].isoformat()
            }
        )

        response = self.client.post(
            reverse('appointment-list'),
            appointment_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Appointment.objects.count(), 1)

    @patch('app.validators.datetime')
    def test_create_appointment_unauthenticated(self, mock_datetime):
        mock_datetime.now.return_value = self.mock_datetime
        self.client.force_authenticate(user=None)

        appointment_data = (
            self.appointment_args
            |
            {
                "business": self.business.id,
                "customer": self.customer.id,
                "service": self.service.id,
                "professional": self.professional.id,
                "datetime": self.appointment_args["datetime"].isoformat()
            }
        )
        response = self.client.post(
            reverse('appointment-list'),
            appointment_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('app.validators.datetime')
    def test_create_appointment_with_invalid_field(self, mock_datetime):
        mock_datetime.now.return_value = self.mock_datetime

        appointment_data = (
            self.appointment_args
            |
            {
                "business": self.business.id,
                "customer": self.customer.id,
                "service": self.service.id,
                "professional": self.professional.id,
                "datetime": self.appointment_args["datetime"].isoformat(),
                "source": "APP"
            }
        )
        response = self.client.post(
            reverse('appointment-list'),
            appointment_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('app.validators.datetime')
    def test_refuse_duplicate_appointment(self, mock_datetime):
        mock_datetime.now.return_value = self.mock_datetime
        appointment_data = (
            self.appointment_args
            |
            {
                "business": self.business.id,
                "customer": self.customer.id,
                "service": self.service.id,
                "professional": self.professional.id,
                "datetime": self.appointment_args["datetime"].isoformat()
            }
        )

        response = self.client.post(
            reverse('appointment-list'),
            appointment_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        other_appointment_data = appointment_data | {"source": "WEBSITE"}
        response = self.client.post(
            reverse('appointment-list'),
            other_appointment_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('app.validators.datetime')
    def test_update_appointment_field(self, mock_datetime):
        mock_datetime.now.return_value = self.mock_datetime
        appointment = Appointment.objects.create(**self.appointment_args)
        updated_field = {
            "datetime": (
                (self.appointment_args["datetime"] + timedelta(days=1))
                .isoformat()
            )
        }
        
        response = self.client.patch(
            reverse('appointment-detail', args=[appointment.id]),
            updated_field,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Appointment.objects.count(), 1)
        self.assertEqual(
            Appointment.objects.get(id=appointment.id).datetime,
            datetime.fromisoformat(updated_field["datetime"])
        )

    @patch('app.validators.datetime')
    def test_update_appointment_field_unauthenticated(self, mock_datetime):
        mock_datetime.now.return_value = self.mock_datetime
        self.client.force_authenticate(user=None)
        appointment = Appointment.objects.create(**self.appointment_args)

        updated_field = {
            "datetime": (
                (self.appointment_args["datetime"] + timedelta(days=1))
                .isoformat()
            )
        }
        
        response = self.client.patch(
            reverse('appointment-detail', args=[appointment.id]),
            updated_field,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('app.validators.datetime')
    def test_delete_appointment(self, mock_datetime):
        mock_datetime.now.return_value = self.mock_datetime
        appointment = Appointment.objects.create(**self.appointment_args)

        response = self.client.delete(
            reverse('appointment-detail', args=[appointment.id])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Appointment.objects.count(), 0)

    @patch('app.validators.datetime')
    def test_delete_appointment_unauthenticated(self, mock_datetime):
        mock_datetime.now.return_value = self.mock_datetime
        self.client.force_authenticate(user=None)
        appointment = Appointment.objects.create(**self.appointment_args)

        response = self.client.delete(
            reverse('appointment-detail', args=[appointment.id])
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
