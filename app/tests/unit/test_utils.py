from app.utils import (
    standardize_numeric_string,
    standardize_email,
    Source,
    AppointmentStatus,
    BusinessCategory
)
from unittest import TestCase


class TestUtils(TestCase):

    def test_standardize_numeric_string(self):
        self.assertEqual(standardize_numeric_string("123.456.789-00 "), "12345678900")
        self.assertEqual(standardize_numeric_string("(11) 99595-4250"), "11995954250")
        self.assertEqual(standardize_numeric_string("+55 11 995954250"), "5511995954250")

    def test_standardize_email(self):
        self.assertEqual(standardize_email("Username@teste.com "), "username@teste.com")
        self.assertEqual(standardize_email("USERNAME@TESTE.COM"), "username@teste.com")

    def test_source_validation(self):
        self.assertTrue(Source.is_valid("whatsapp"))
        self.assertTrue(Source.is_valid("WEBSITE"))
        self.assertFalse(Source.is_valid("app"))

    def test_appointment_status_validation(self):
        self.assertTrue(AppointmentStatus.is_valid("SCHEDULED"))
        self.assertTrue(AppointmentStatus.is_valid("confirmed"))
        self.assertTrue(AppointmentStatus.is_valid("CANCELLED"))
        self.assertTrue(AppointmentStatus.is_valid("completed"))
        self.assertFalse(AppointmentStatus.is_valid("FINISHED"))

    def test_business_category_validation(self):
        self.assertTrue(BusinessCategory.is_valid("C1"))
        self.assertTrue(BusinessCategory.is_valid("c3"))
        self.assertFalse(BusinessCategory.is_valid("C50"))