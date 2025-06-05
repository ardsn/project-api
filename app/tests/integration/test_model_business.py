from django.test import TestCase
from django.core.exceptions import ValidationError
from app.models import Business, City


class TestBusinessModel(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.city = City.objects.get(name="Ariquemes", state="RO")

    def test_validate_category(self):
        fixed_params = {
            "city": self.city,
            "address": "Rua 1",
            "public_phone": "(89) 99595-4250",
            "restricted_phone": "(89) 99595-4250",
            "email": "clinica@fagundes.com",
            "schedule": {
                "0": {
                    "start": "08:00",
                    "end": "17:00",
                    "breaks": []
                }
            },
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

    def test_validate_public_phone(self):
        fixed_params = {
            "city": self.city,
            "address": "Rua 1",
            "restricted_phone": "(89) 99595-4250",
            "email": "clinica@fagundes.com",
            "schedule": {
                "0": {
                    "start": "08:00",
                    "end": "17:00",
                    "breaks": []
                }
            },
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

    def test_validate_restricted_phone(self):
        fixed_params = {
            "city": self.city,
            "address": "Rua 1",
            "public_phone": "(89) 99595-4250",
            "email": "clinica@fagundes.com",
            "schedule": {
                "0": {
                    "start": "08:00",
                    "end": "17:00",
                    "breaks": []
                }
            },
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
        
    def test_validate_schedule(self):
        with self.assertRaises(ValidationError):
            Business.objects.create(
                name="NAME",
                city=self.city,
                address="Rua 1",
                public_phone="(89) 99595-4250",
                restricted_phone="(89) 99595-4250",
                email="clinica@fagundes.com",
                closed_on_holidays=True,
                category="C1",
                schedule={
                    "0": {
                            "start": "08:00",
                            "end": "17:00",
                            "breaks": [
                                {"start": "17:00", "end": "18:00"}
                            ]
                    }
                }
            )
            
    def test_unique_constraint(self):
        params = {
            "name": "NAME",
            "category": "C1",
            "city": self.city,
            "address": "Rua 1",
            "public_phone": "(89) 99595-4250",
            "restricted_phone": "(89) 99595-4250",
            "email": "clinica@fagundes.com",
            "schedule": {
                "0": {
                    "start": "08:00",
                    "end": "17:00",
                    "breaks": []
                }
            },
            "closed_on_holidays": True
        }

        business = Business.objects.create(**params)
        self.assertIsInstance(business, Business)

        with self.assertRaises(ValidationError):
            Business.objects.create(**params)
