import unittest
from unittest.mock import patch
from django.core.exceptions import ValidationError
from app.utils import validate_cpf, standardize_numeric_string, standardize_email
from app.models import City
from django.core.management import call_command
import httpx


class TestUtils(unittest.TestCase):

    def test_validate_cpf(self):
        self.assertIsNone(validate_cpf("111.444.777-35"))

        with self.assertRaises(ValidationError, msg="Invalid CPF! Verifier digits are invalid."):
            validate_cpf("123.456.789-00")

        with self.assertRaises(ValidationError, msg="Invalid CPF! It must have 11 digits."):
            validate_cpf("123.456.789")

        with self.assertRaises(ValidationError, msg="Invalid CPF! All digits are the same."):
            validate_cpf("111.111.111-11")

    def test_standardize_numeric_string(self):
        self.assertEqual(standardize_numeric_string("123.456.789-00 "), "12345678900")
        self.assertEqual(standardize_numeric_string("(11) 99595-4250"), "11995954250")
        self.assertEqual(standardize_numeric_string("+55 11 995954250"), "5511995954250")

    def test_standardize_email(self):
        self.assertEqual(standardize_email("Username@teste.com "), "username@teste.com")
        self.assertEqual(standardize_email("USERNAME@TESTE.COM"), "username@teste.com")


class TestDataMigration(unittest.TestCase):

    def test_migration_with_mocked_httpx(self):
        def mock_send(request):
            json_data = [
                {
                    "nome": "Cidade1",
                    "regiao-imediata": {
                        "regiao-intermediaria": {"UF": {"sigla": "RO"}}
                    }
                },
                {
                    "nome": "Cidade2",
                    "regiao-imediata": {
                        "regiao-intermediaria": {"UF": {"sigla": "MG"}}
                    }
                }
            ]
            return httpx.Response(200, json=json_data)

        transport = httpx.MockTransport(mock_send)
        OriginalClient = httpx.Client

        def mock_client(*args, **kwargs):
            return OriginalClient(transport=transport)

        with patch("httpx.Client", mock_client):
            call_command("migrate", "app", "0002")

        self.assertEqual(City.objects.count(), 2)
        self.assertEqual(City.objects.get(name="Cidade1").state, "RO")
        self.assertEqual(City.objects.get(name="Cidade2").state, "MG")

        call_command("migrate", "app", "0001")
        self.assertEqual(City.objects.count(), 0)


if __name__ == "__main__":
    unittest.main()