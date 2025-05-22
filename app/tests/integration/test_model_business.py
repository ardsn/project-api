from django.test import TestCase
from django.core.exceptions import ValidationError
from app.models import Business, City


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