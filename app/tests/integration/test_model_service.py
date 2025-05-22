from django.test import TestCase
from django.core.exceptions import ValidationError
from app.models import Service, Business, City
from datetime import timedelta


class TestServiceModel(TestCase):

    def setUp(self) -> None:
        self.business = Business.objects.create(
            name="Clínica Fagundes",
            category="C1",
            city=City.objects.get(name="Ariquemes", state="RO"),
            address="Rua 1",
            public_phone="(12) 3456-7890",
            restricted_phone="(12) 3456-7890",
            email="clinica@fagundes.com",
            schedule={"lunch": {"start": "12:00", "end": "13:00"}},
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

        # Tear down
        service.delete()

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

        # Tear down
        service.delete()

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

        # Tear down
        service.delete()

    def test_standardize_data(self):
        service_one = Service.objects.create(
            business=self.business,
            name="serviço de teste",
            description="Descrição do serviço",
            price=100.00,
            duration=timedelta(hours=1)
        )

        service_two = Service.objects.create(
            business=self.business,
            name="Outro Serviço",
            description="Descrição do serviço",
            price=800.00,
            duration=timedelta(hours=1)
        )
        self.assertEqual(Service.objects.get(id=1).name, "Serviço de teste")
        self.assertEqual(Service.objects.get(id=2).name, "Outro serviço")

        # Tear down
        service_one.delete()
        service_two.delete()

    def tearDown(self) -> None:
        Service.objects.all().delete()
        self.business.delete()