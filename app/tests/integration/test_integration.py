from django.test import TestCase
from app.models import Business, City


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
