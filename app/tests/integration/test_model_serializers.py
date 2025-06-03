from app.serializers import AvailableDaySerializer
from app.models import Business, City, Professional
from django.test import TestCase
from datetime import time, datetime
from zoneinfo import ZoneInfo
from unittest.mock import patch

class TestAvailableDayModelSerializer(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.now: datetime = (
            datetime
            .now(tz=ZoneInfo("America/Sao_Paulo"))
        )

        cls.business = Business.objects.create(
            name="Clínica Fagundes",
            category="C1",
            city=City.objects.get(name="Ariquemes", state="RO"),
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
            business=cls.business,
            name="JOÃO DA SILVA",
            cpf="111.444.777-35",
            speciality="cardiologista",
            email="Joao.silva@example.com",
            phone="(21) 3456-7890",
            schedule={
                "0": {
                    "start": "08:00",
                    "end": "17:00",
                    "breaks": []
                }
            }
        )

    @patch("app.validators.datetime")
    def test_validate_blocked_times(self, mock_datetime):
        mock_datetime.now.return_value = self.now

        serializer = AvailableDaySerializer(data={
            'business': self.business.id,
            'professional': self.professional.id,
            'date': self.now.date(),
            'blocked_start_time': time(10, 0),
            'blocked_end_time': time(11, 0)
        })
        serializer.is_valid()
        self.assertTrue(serializer.is_valid())

        serializer = AvailableDaySerializer(data={
            'business': self.business.id,
            'professional': self.professional.id,
            'date': self.now.date(),
            'blocked_start_time': time(11, 0),
            'blocked_end_time': time(11, 0)
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)
        self.assertEqual(
            serializer.errors['non_field_errors'][0],
            'The blocked start time must be before the blocked end time'
        )

        serializer = AvailableDaySerializer(data={
            'business': self.business.id,
            'professional': self.professional.id,
            'date': self.now.date(),
            'blocked_start_time': time(10, 0),
            'blocked_end_time': None
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)
        self.assertEqual(
            serializer.errors['non_field_errors'][0],
            'Both blocked_start_time and blocked_end_time must be provided together'
        )
