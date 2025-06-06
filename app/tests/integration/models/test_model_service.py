from django.test import TestCase
from django.core.exceptions import ValidationError
from app.models import Service, Business, City
from datetime import timedelta


class TestServiceModel(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
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

    def test_validate_price(self):
        fixed_params = {
            "business": self.business,
            "name": "Serviço de teste",
            "description": "Descrição do serviço",
            "duration": timedelta(hours=1)
        }

        service = Service.objects.create(**fixed_params, price=100.00)
        self.assertIsInstance(service, Service)

        with self.assertRaises(ValidationError):
            Service.objects.create(**fixed_params, price=-100.00)

    def test_validate_duration(self):
        fixed_params = {
            "business": self.business,
            "name": "Serviço de teste",
            "description": "Descrição do serviço",
            "price": 100.00
        }

        service = Service.objects.create(**fixed_params, duration=timedelta(seconds=60))
        self.assertIsInstance(service, Service)

        with self.assertRaises(ValidationError):
            Service.objects.create(**fixed_params, duration=timedelta(seconds=59))

    def test_unique_constraint(self):
        params = {
            "business": self.business,
            "name": "Serviço de teste",
            "description": "Descrição do serviço",
            "price": 100.00,
            "duration": timedelta(seconds=60)
        }

        service = Service.objects.create(**params)
        self.assertIsInstance(service, Service)

        with self.assertRaises(ValidationError):
            Service.objects.create(**params)
