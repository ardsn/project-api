from django.test import TestCase
from django.core.exceptions import ValidationError
from app.models import Appointment, Business, Customer, Service, Professional, City
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from unittest.mock import patch


class TestAppointmentModel(TestCase):

    def setUp(self) -> None:
        self.now = datetime.now(ZoneInfo("America/Sao_Paulo"))
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

        self.professional = Professional.objects.create(
            business=self.business,
            name="JOÃO DA SILVA",
            cpf="111.444.777-35",
            speciality="cardiologista",
            email="Joao.silva@example.com",
            phone="(21) 3456-7890",
            schedule={"lunch": {"start": "12:00", "end": "13:00"}}
        )

        self.customer = Customer.objects.create(
            business=self.business,
            name="João da Silva",
            email="JOAO.SILVA@EXAMPLE.COM",
            phone="(21) 3456-7890",
            cpf="111.444.777-35",
            registration_source="website"
        )

        self.service = Service.objects.create(
            business=self.business,
            name="serviço de teste",
            description="Descrição do serviço",
            price=100.00,
            duration=timedelta(hours=1)
        )


    @patch("app.validators.datetime")
    def test_validate_datetime(self, mock_datetime):
        mock_datetime.now.return_value = self.now

        fixed_params = {
            "business": self.business,
            "customer": self.customer,
            "service": self.service,
            "professional": self.professional,
            "source": "whatsapp"
        }

        appointment = Appointment.objects.create(
            **fixed_params,
            datetime=self.now + timedelta(days=1)
        )
        self.assertIsInstance(appointment, Appointment)

        with self.assertRaises(ValidationError):
            Appointment.objects.create(
                **fixed_params,
                datetime=self.now - timedelta(minutes=10)
            )

        # Tear down
        appointment.delete()

    def test_validate_status(self):
        fixed_params = {
            "business": self.business,
            "customer": self.customer,
            "service": self.service,
            "professional": self.professional,
            "datetime": self.now + timedelta(days=1),
            "source": "website"
        }

        appointment = Appointment.objects.create(
            **fixed_params,
            status="completed"
        )
        self.assertIsInstance(appointment, Appointment)

        with self.assertRaises(ValidationError):
            Appointment.objects.create(
                **fixed_params,
                status="FINISHED"
            )

        # Tear down
        appointment.delete()

    def test_validate_source(self):
        fixed_params = {
            "business": self.business,
            "customer": self.customer,
            "service": self.service,
            "professional": self.professional,
            "datetime": self.now + timedelta(days=1),
            "status": "SCHEDULED"
        }

        appointment = Appointment.objects.create(
            **fixed_params,
            source="whatsapp"
        )
        self.assertIsInstance(appointment, Appointment)

        with self.assertRaises(ValidationError):
            Appointment.objects.create(
                **fixed_params,
                source="APP"
            )

        # Tear down
        appointment.delete()

    def test_unique_constraint(self):
        params = {
            "business": self.business,
            "customer": self.customer,
            "service": self.service,
            "professional": self.professional,
            "datetime": self.now + timedelta(days=1),
            "status": "SCHEDULED",
            "source": "WEBSITE"
        }

        appointment = Appointment.objects.create(**params)
        self.assertIsInstance(appointment, Appointment)

        with self.assertRaises(ValidationError):
            Appointment.objects.create(**params)

        # Tear down
        appointment.delete()

    def test_standardize_data(self):

        appointment = Appointment.objects.create(
            business=self.business,
            customer=self.customer,
            service=self.service,
            professional=self.professional,
            datetime=self.now + timedelta(days=1),
            status="Scheduled",
            source="website"
        )

        self.assertIsInstance(appointment, Appointment)
        self.assertEqual(Appointment.objects.get(id=1).status, "SCHEDULED")
        self.assertEqual(Appointment.objects.get(id=1).source, "WEBSITE")

        # Tear down
        appointment.delete()

    def tearDown(self) -> None:
        Appointment.objects.all().delete()
        self.customer.delete()
        self.service.delete()
        self.professional.delete()
        self.business.delete()