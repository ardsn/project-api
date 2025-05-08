from app.models import City
from unittest import TestCase
from unittest.mock import patch
import httpx
from django.core.management import call_command


class TestDataMigration(TestCase):

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

        with patch('httpx.Client', mock_client):
            call_command('migrate', 'app', '0002')

        self.assertEqual(City.objects.count(), 2)
        self.assertEqual(City.objects.get(name="Cidade1").state, "RO")
        self.assertEqual(City.objects.get(name="Cidade2").state, "MG")

        call_command('migrate', 'app', '0001')
        self.assertEqual(City.objects.count(), 0)
