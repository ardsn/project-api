from app.validators import (
    validate_phone_number,
    validate_cpf,
    validate_date,
    validate_datetime,
    validate_price,
    validate_duration,
    validate_source,
    validate_status,
    validate_business_category
)
from datetime import date, datetime, timedelta
from unittest import TestCase
from unittest.mock import patch
from django.core.exceptions import ValidationError


class TestValidators(TestCase):
    
    def test_validate_cpf(self):
        self.assertIsNone(validate_cpf("111.444.777-35"))

        with self.assertRaises(ValidationError, msg="Invalid CPF! Verifier digits are invalid."):
            validate_cpf("123.456.789-00")

        with self.assertRaises(ValidationError, msg="Invalid CPF! It must have 11 digits."):
            validate_cpf("123.456.789")

        with self.assertRaises(ValidationError, msg="Invalid CPF! All digits are the same."):
            validate_cpf("111.111.111-11")

    @patch("app.validators.datetime")
    def test_validate_date(self, mock_datetime):
        mock_datetime.now.side_effect = lambda *args, **kwargs: datetime(2025, 1, 2)

        self.assertIsNone(validate_date(date(2025, 1, 2)))
        self.assertIsNone(validate_date(date(2025, 1, 4)))

        with self.assertRaises(ValidationError):
            validate_date(date(2025, 1, 1))

    @patch("app.validators.datetime")
    def test_validate_datetime(self, mock_datetime):
        mock_datetime.now.side_effect = lambda *args, **kwargs: datetime(2025, 1, 2, 10, 0, 0)

        self.assertIsNone(validate_datetime(datetime(2025, 1, 2, 10, 30, 0)))

        with self.assertRaises(ValidationError):
            validate_datetime(datetime(2025, 1, 2, 9, 59, 0))

    def test_validate_price(self):
        self.assertIsNone(validate_price(50))
        self.assertIsNone(validate_price(0))

        with self.assertRaises(ValidationError):
            validate_price(-100)

    def test_validate_duration(self):
        self.assertIsNone(validate_duration(timedelta(minutes=1)))
        self.assertIsNone(validate_duration(timedelta(minutes=60)))

        with self.assertRaises(ValidationError):
            validate_duration(timedelta(seconds=59.0))

    def test_validate_source(self):
        self.assertIsNone(validate_source("whatsapp"))
        self.assertIsNone(validate_source("WEBSITE"))

        with self.assertRaises(ValidationError):
            validate_source("app")

    def test_validate_status(self):
        self.assertIsNone(validate_status("scheduled"))
        self.assertIsNone(validate_status("CONFIRMED"))

        with self.assertRaises(ValidationError):
            validate_status("FINISHED")

    def test_validate_business_category(self):
        self.assertIsNone(validate_business_category("C5"))
        self.assertIsNone(validate_business_category("c1"))

        with self.assertRaises(ValidationError):
            validate_business_category("C50")

    def test_validate_phone_number(self):
        self.assertIsNone(validate_phone_number("11995954250"))
        self.assertIsNone(validate_phone_number("(89) 99595-4250"))
        self.assertIsNone(validate_phone_number("11 99595-4250"))
        self.assertIsNone(validate_phone_number("(21) 3456-7890"))
        self.assertIsNone(validate_phone_number("2134567890"))
        self.assertIsNone(validate_phone_number("98 3456-7890"))

        with self.assertRaises(ValidationError, msg="Phone number must have 10 or 11 digits."):
            validate_phone_number("+55 11 995954250")

        with self.assertRaises(ValidationError, msg="Phone number must have 10 or 11 digits."):
            validate_phone_number("(11) 959-4250")

        with self.assertRaises(ValidationError, msg="Invalid area code (DDD)."):
            validate_phone_number("(00) 94959-4250")

        with self.assertRaises(ValidationError, msg="Invalid area code (DDD)."):
            validate_phone_number("(100) 4959-4250")

        with self.assertRaises(ValidationError, msg="Mobile numbers must start with 9 after the area code."):
            validate_phone_number("(89) 89595-4250")

        with self.assertRaises(ValidationError, msg="Landline numbers must start with 2, 3, 4, or 5 after the area code."):
            validate_phone_number("(11) 1595-4250")

        with self.assertRaises(ValidationError, msg="Landline numbers must start with 2, 3, 4, or 5 after the area code."):
            validate_phone_number("(11) 6595-4250")