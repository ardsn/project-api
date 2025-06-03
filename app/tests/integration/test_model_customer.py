from django.test import TestCase
from django.core.exceptions import ValidationError
from app.models import Customer, Business, City


class TestCustomerModel(TestCase):

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
