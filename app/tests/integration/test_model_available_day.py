from django.test import TestCase
from django.core.exceptions import ValidationError
from app.models import AvailableDay, Business, Professional, City
from datetime import datetime, timedelta, date
from zoneinfo import ZoneInfo


class TestAvailableDayModel(TestCase):

    def setUp(self) -> None:
        self.today: date = (
            datetime
            .now(tz=ZoneInfo("America/Sao_Paulo"))
            .date()
        )

        self.business = Business.objects.create(
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

        self.professional = Professional.objects.create(
            business=self.business,
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

    def test_validate_date(self):
        fixed_params = {
            "business": self.business,
            "professional": self.professional
        }

        available_day = AvailableDay.objects.create(
            **fixed_params,
            date=self.today
        )
        self.assertIsInstance(available_day, AvailableDay)

        with self.assertRaises(ValidationError):
            AvailableDay.objects.create(
                **fixed_params,
                date=self.today - timedelta(days=1)
            )

        # Tear down
        available_day.delete()

    def test_unique_constraint(self):
        params = {
            "business": self.business,
            "professional": self.professional,
            "date": self.today
        }

        available_day = AvailableDay.objects.create(**params)
        self.assertIsInstance(available_day, AvailableDay)

        with self.assertRaises(ValidationError):
            AvailableDay.objects.create(**params)

        # Tear down
        available_day.delete()

    def tearDown(self) -> None:
        AvailableDay.objects.all().delete()
        self.business.delete()
        self.professional.delete()