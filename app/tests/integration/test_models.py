from app.models import (
    Business,
    City,
    Customer,
    Service,
    Professional,
    Appointment,
    AvailableDay
)
from datetime import timedelta, datetime, timezone, date
from unittest.mock import patch
from zoneinfo import ZoneInfo
from django.test import TestCase
from django.core.exceptions import ValidationError


class TestCityModel(TestCase):

    def test_unique_constraint(self):
        with self.assertRaises(ValidationError):
            City.objects.create(name="Ariquemes", state="RO")


class TestBusinessModel(TestCase):

    def setUp(self) -> None:
        self.city = City.objects.get(name="Ariquemes", state="RO")

    def test_validate_category(self):
        fixed_params = {
            "city": self.city,
            "address": "Rua 1",
            "public_phone": "(89) 99595-4250",
            "restricted_phone": "(89) 99595-4250",
            "email": "clinica@fagundes.com",
            "schedule": {"lunch": {"start": "12:00", "end": "13:00"}},
            "closed_on_holidays": True
        }

        business = Business.objects.create(
            name="NAME1",
            category="C6",
            **fixed_params
        )
        self.assertIsInstance(business, Business)

        with self.assertRaises(ValidationError):
            Business.objects.create(
                name="NAME2",
                category="C17",
                **fixed_params
            )
        
        # Tear down
        business.delete()

    def test_validate_public_phone(self):
        fixed_params = {
            "city": self.city,
            "address": "Rua 1",
            "restricted_phone": "(89) 99595-4250",
            "email": "clinica@fagundes.com",
            "schedule": {"lunch": {"start": "12:00", "end": "13:00"}},
            "closed_on_holidays": True,
            "category": "C1"
        }

        business = Business.objects.create(
            name="NAME1",
            public_phone="(89) 99595-4250",
            **fixed_params
        )
        self.assertIsInstance(business, Business)

        with self.assertRaises(ValidationError):
            Business.objects.create(
                name="NAME2",
                public_phone="+55 11 995954250",
                **fixed_params
            )

        # Tear down
        business.delete()

    def test_validate_restricted_phone(self):
        fixed_params = {
            "city": self.city,
            "address": "Rua 1",
            "public_phone": "(89) 99595-4250",
            "email": "clinica@fagundes.com",
            "schedule": {"lunch": {"start": "12:00", "end": "13:00"}},
            "closed_on_holidays": True,
            "category": "C1"
        }

        business = Business.objects.create(
            name="NAME1",
            restricted_phone="(89) 99595-4250",
            **fixed_params
        )
        self.assertIsInstance(business, Business)

        with self.assertRaises(ValidationError):
            Business.objects.create(
                name="NAME2",
                restricted_phone="+55 11 995954250",
                **fixed_params
            )

        # Tear down
        business.delete()

    def test_unique_constraint(self):
        params = {
            "name": "NAME",
            "category": "C1",
            "city": self.city,
            "address": "Rua 1",
            "public_phone": "(89) 99595-4250",
            "restricted_phone": "(89) 99595-4250",
            "email": "clinica@fagundes.com",
            "schedule": {"lunch": {"start": "12:00", "end": "13:00"}},
            "closed_on_holidays": True
        }

        business = Business.objects.create(**params)
        self.assertIsInstance(business, Business)

        with self.assertRaises(ValidationError):
            Business.objects.create(**params)

        # Tear down
        business.delete()

    def test_standardize_data(self):
        business = Business.objects.create(
            name="clínica fagundes",
            category="C1",
            city=self.city,
            address="Rua 1",
            public_phone="(12) 3456-7890",
            restricted_phone="(12) 3456-7890",
            email="CLINICA@FAGUNDES.COM ",
            schedule={"lunch": {"start": "12:00", "end": "13:00"}},
            closed_on_holidays=False
        )
        self.assertEqual(Business.objects.get(id=1).name, "Clínica Fagundes")
        self.assertEqual(Business.objects.get(id=1).public_phone, "1234567890")
        self.assertEqual(Business.objects.get(id=1).restricted_phone, "1234567890")
        self.assertEqual(Business.objects.get(id=1).email, "clinica@fagundes.com")

        # Tear down
        business.delete()

    def tearDown(self) -> None:
        Business.objects.all().delete()


class TestCustomerModel(TestCase):

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

    def test_validate_registration_source(self):
        fixed_params = {
            "business": self.business,
            "name": "João da Silva",
            "email": "joao.silva@example.com",
            "phone": "(89) 99595-4250",
            "cpf": "111.444.777-35"
        }

        customer = Customer.objects.create(**fixed_params, registration_source="WEBSITE")
        self.assertIsInstance(customer, Customer)

        with self.assertRaises(ValidationError):
            Customer.objects.create(
                **fixed_params,
                registration_source="APP"
            )

        # Tear down
        customer.delete()

    def test_validate_cpf(self):
        fixed_params = {
            "business": self.business,
            "name": "João da Silva",
            "email": "joao.silva@example.com",
            "phone": "(89) 99595-4250",
            "registration_source": "WHATSAPP"
        }

        customer = Customer.objects.create(**fixed_params, cpf="111.444.777-35")
        self.assertIsInstance(customer, Customer)

        with self.assertRaises(ValidationError):
            Customer.objects.create(**fixed_params, cpf="123.456.789-00")

        # Tear down
        customer.delete()

    def test_validate_phone(self):
        fixed_params = {
            "business": self.business,
            "name": "João da Silva",
            "email": "joao.silva@example.com",
            "cpf": "111.444.777-35",
            "registration_source": "WHATSAPP"
        }

        customer = Customer.objects.create(**fixed_params, phone="11995954250")
        self.assertIsInstance(customer, Customer)

        with self.assertRaises(ValidationError):
            Customer.objects.create(**fixed_params, phone="(11) 1595-4250")

        # Tear down
        customer.delete()

    def test_unique_constraint(self):
        params = {
            "business": self.business,
            "name": "João da Silva",
            "email": "joao.silva@example.com",
            "phone": "11995954250",
            "cpf": "111.444.777-35",
            "registration_source": "WHATSAPP"
        }

        customer = Customer.objects.create(**params)
        self.assertIsInstance(customer, Customer)

        with self.assertRaises(ValidationError):
            Customer.objects.create(**params)

        # Tear down
        customer.delete()

    def test_standardize_data(self):
        customer = Customer.objects.create(
            business=self.business,
            name="João da Silva",
            email="JOAO.SILVA@EXAMPLE.COM ",
            phone="(21) 3456-7890",
            cpf="111.444.777-35",
            registration_source="website"
        )
        self.assertEqual(Customer.objects.get(id=1).name, "João Da Silva")
        self.assertEqual(Customer.objects.get(id=1).registration_source, "WEBSITE")
        self.assertEqual(Customer.objects.get(id=1).email, "joao.silva@example.com")
        self.assertEqual(Customer.objects.get(id=1).phone, "2134567890")
        self.assertEqual(Customer.objects.get(id=1).cpf, "11144477735")

        # Tear down
        customer.delete()

    def tearDown(self) -> None:
        Customer.objects.all().delete()
        self.business.delete()

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


class TestProfessionalModel(TestCase):

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

    def test_validate_cpf(self):
        fixed_params = {
            "business": self.business,
            "name": "Caio Medeiros",
            "email": "caio.medeiros@example.com",
            "phone": "11995954250",
            "speciality": "Cardiologista",
            "schedule": {"lunch": {"start": "12:00", "end": "13:00"}}
        }

        professional = Professional.objects.create(**fixed_params, cpf="111.444.777-35")
        self.assertIsInstance(professional, Professional)

        with self.assertRaises(ValidationError):
            Professional.objects.create(**fixed_params, cpf="111.111.111-11")

        # Tear down
        professional.delete()

    def test_unique_constraint(self):
        params = {
            "business": self.business,
            "name": "Caio Medeiros",
            "email": "caio.medeiros@example.com",
            "phone": "11995954250",
            "cpf": "111.444.777-35",
            "speciality": "Cardiologista",
            "schedule": {"lunch": {"start": "12:00", "end": "13:00"}}
        }

        professional = Professional.objects.create(**params)
        self.assertIsInstance(professional, Professional)

        with self.assertRaises(ValidationError):
            Professional.objects.create(**params)

        # Tear down
        professional.delete()

    def test_standardize_data(self):
        professional = Professional.objects.create(
            business=self.business,
            name="JOÃO DA SILVA",
            cpf="111.444.777-35 ",
            speciality="cardiologista",
            email="Joao.silva@example.com ",
            phone="(21) 3456-7890",
            schedule={"lunch": {"start": "12:00", "end": "13:00"}}
        )

        self.assertEqual(Professional.objects.get(id=1).name, "João Da Silva")
        self.assertEqual(Professional.objects.get(id=1).cpf, "11144477735")
        self.assertEqual(Professional.objects.get(id=1).speciality, "Cardiologista")
        self.assertEqual(Professional.objects.get(id=1).email, "joao.silva@example.com")
        self.assertEqual(Professional.objects.get(id=1).phone, "2134567890")

        # Tear down
        professional.delete()

    def tearDown(self) -> None:
        Professional.objects.all().delete()
        self.business.delete()


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
        Customer.objects.all().delete()
        Service.objects.all().delete()
        Professional.objects.all().delete()
        Business.objects.all().delete()