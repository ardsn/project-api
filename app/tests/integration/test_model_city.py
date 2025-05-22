from app.models import City
from django.test import TestCase
from django.core.exceptions import ValidationError


class TestCityModel(TestCase):

    def test_unique_constraint(self):
        with self.assertRaises(ValidationError):
            City.objects.create(name="Ariquemes", state="RO")
