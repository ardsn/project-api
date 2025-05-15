from app.models import (
    Business,
    City,
    Customer,
    Service,
    Professional,
    Appointment
)
from datetime import timedelta, datetime, timezone
from django.test import TestCase


class TestBusinessModel(TestCase):

    def test_save_business(self):
        city = City.objects.get(name="Ariquemes")
        Business.objects.create(
            name="clínica fagundes",
            category="C1",
            state="RO",
            city=city,
            address="Rua 1",
            public_phone="(12) 3456-7890",
            restricted_phone="(12) 3456-7890",
            email="CLINICA@FAGUNDES.COM ",
            schedule={},
            closed_on_holidays=False
        )
        self.assertEqual(Business.objects.get(id=1).name, "Clínica Fagundes")
        self.assertEqual(Business.objects.get(id=1).public_phone, "1234567890")
        self.assertEqual(Business.objects.get(id=1).restricted_phone, "1234567890")
        self.assertEqual(Business.objects.get(id=1).email, "clinica@fagundes.com")


    def tearDown(self) -> None:
        Business.objects.all().delete()


class TestCustomerModel(TestCase):

    def test_save_customer(self):
        business = Business.objects.create(
            name="Clínica Fagundes",
            category="C1",
            state="RO",
            city=City.objects.get(name="Ariquemes"),
            address="Rua 1",
            schedule={},
            closed_on_holidays=False
        )
        Customer.objects.create(
            business=business,
            name="João da Silva",
            email="JOAO.SILVA@EXAMPLE.COM ",
            phone="(55) 12345-6789",
            cpf="123.456.789-01",
            registration_source="WEBSITE"
        )
        self.assertEqual(Customer.objects.get(id=1).name, "João Da Silva")
        self.assertEqual(Customer.objects.get(id=1).registration_source, "website")
        self.assertEqual(Customer.objects.get(id=1).email, "joao.silva@example.com")
        self.assertEqual(Customer.objects.get(id=1).phone, "55123456789")
        self.assertEqual(Customer.objects.get(id=1).cpf, "12345678901")

    def tearDown(self) -> None:
        Customer.objects.all().delete()


class TestServiceModel(TestCase):

    def test_save_service(self):
        business = Business.objects.create(
            name="Clínica Fagundes",
            category="C1",
            state="RO",
            city=City.objects.get(name="Ariquemes"),
            address="Rua 1",
            public_phone="(12) 3456-7890",
            restricted_phone="(12) 3456-7890",
            email="CLINICA@FAGUNDES.COM ",
            schedule={},
            closed_on_holidays=False
        )
        
        Service.objects.create(
            business=business,
            name="serviço de teste",
            description="Descrição do serviço",
            price=100.00,
            duration=timedelta(hours=1)
        )

        Service.objects.create(
            business=business,
            name="Outro Serviço",
            description="Descrição do serviço",
            price=800.00,
            duration=timedelta(hours=1)
        )
        self.assertEqual(Service.objects.get(id=1).name, "Serviço de teste")
        self.assertEqual(Service.objects.get(id=2).name, "Outro serviço")


    def tearDown(self) -> None:
        Service.objects.all().delete()
        Business.objects.all().delete()


class TestProfessionalModel(TestCase):

    def test_save_professional(self):
        business = Business.objects.create(
            name="Clínica Fagundes",
            category="C1",
            state="RO",
            city=City.objects.get(name="Ariquemes"),
            address="Rua 1",
            public_phone="(12) 3456-7890",
            restricted_phone="(12) 3456-7890",
            email="clinica@fagundes.com ",
            schedule={},
            closed_on_holidays=False
        )

        Professional.objects.create(
            business=business,
            name="JOÃO DA SILVA",
            cpf="123.456.789-01",
            speciality="cardiologista",
            email="Joao.silva@example.com ",
            phone="+5511 12345-6789",
            schedule={}
        )

        self.assertEqual(Professional.objects.get(id=1).name, "João Da Silva")
        self.assertEqual(Professional.objects.get(id=1).cpf, "12345678901")
        self.assertEqual(Professional.objects.get(id=1).speciality, "Cardiologista")
        self.assertEqual(Professional.objects.get(id=1).email, "joao.silva@example.com")
        self.assertEqual(Professional.objects.get(id=1).phone, "5511123456789")

    def tearDown(self) -> None:
        Professional.objects.all().delete()
        Business.objects.all().delete()


class TestAppointmentModel(TestCase):

    def test_save_appointment(self):
        business = Business.objects.create(
            name="Clínica Fagundes",
            category="C1",
            state="RO",
            city=City.objects.get(name="Ariquemes"),
            address="Rua 1",
            public_phone="(12) 3456-7890",
            restricted_phone="(12) 3456-7890",
            email="clinica@fagundes.com ",
            schedule={},
            closed_on_holidays=False
        )

        customer = Customer.objects.create(
            business=business,
            name="João da Silva",
            email="joao.silva@example.com",
            phone="+5511 12345-6789",
            cpf="123.456.789-01",
            registration_source="WEBSITE"
        )

        service = Service.objects.create(
            business=business,
            name="Serviço de teste",
            description="Descrição do serviço",
            price=100.00,
            duration=timedelta(hours=1)
        )

        professional = Professional.objects.create(
            business=business,
            name="João da Silva",
            cpf="123.456.789-01",
            speciality="Cardiologista", 
            email="joao.silva@example.com",
            phone="+5511 12345-6789",
            schedule={}
        )

        _ = Appointment.objects.create(
            business=business,
            customer=customer,
            service=service,
            professional=professional,
            datetime=datetime.now(timezone.utc),
            status="Scheduled",
            source="WEBSITE"
        )

        self.assertEqual(Appointment.objects.get(id=1).status, "scheduled")
        self.assertEqual(Appointment.objects.get(id=1).source, "website")

    def tearDown(self) -> None:
        Appointment.objects.all().delete()
        Customer.objects.all().delete()
        Service.objects.all().delete()
        Professional.objects.all().delete()
        Business.objects.all().delete()