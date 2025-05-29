from django.test import TestCase
from django.core.exceptions import ValidationError
from app.models import Professional, Business, City


class TestProfessionalModel(TestCase):

    def setUp(self) -> None:
        self.business = Business.objects.create(
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

    def test_validate_cpf(self):
        fixed_params = {
            "business": self.business,
            "name": "Caio Medeiros",
            "email": "caio.medeiros@example.com",
            "phone": "11995954250",
            "speciality": "Cardiologista",
            "schedule": {
                "0": {
                    "start": "08:00",
                    "end": "17:00",
                    "breaks": []
                }
            }
        }

        professional = Professional.objects.create(**fixed_params, cpf="111.444.777-35")
        self.assertIsInstance(professional, Professional)

        with self.assertRaises(ValidationError):
            Professional.objects.create(**fixed_params, cpf="111.111.111-11")

        # Tear down
        professional.delete()

    def test_validate_schedule(self):
        with self.assertRaises(ValidationError):
            Professional.objects.create(
                business=self.business,
                name="Caio Medeiros",
                cpf="111.444.777-35",
                speciality="Cardiologista",
                email="caio.medeiros@example.com",
                phone="11995954250",
                schedule={
                    "0": {
                        "start": "08:00",
                        "end": "08:00",
                        "breaks": []
                    }
                }
            )
            
    def test_unique_constraint(self):
        params = {
            "business": self.business,
            "name": "Caio Medeiros",
            "email": "caio.medeiros@example.com",
            "phone": "11995954250",
            "cpf": "111.444.777-35",
            "speciality": "Cardiologista",
            "schedule": {
                "0": {
                    "start": "08:00",
                    "end": "17:00",
                    "breaks": []
                }
            }
        }

        professional = Professional.objects.create(**params)
        self.assertIsInstance(professional, Professional)

        with self.assertRaises(ValidationError):
            Professional.objects.create(**params)

        # Tear down
        professional.delete()

    def test_standardize_data(self):
        professional = Professional.objects.create(
            business=self.business,
            name="JOÃO DA SILVA",
            cpf="111.444.777-35 ",
            speciality="cardiologista",
            email="Joao.silva@example.com ",
            phone="(21) 3456-7890",
            schedule={
                "0": {
                    "start": "08:00",
                    "end": "17:00",
                    "breaks": []
                }
            }
        )

        self.assertEqual(Professional.objects.get(id=1).name, "João Da Silva")
        self.assertEqual(Professional.objects.get(id=1).cpf, "11144477735")
        self.assertEqual(Professional.objects.get(id=1).speciality, "Cardiologista")
        self.assertEqual(Professional.objects.get(id=1).email, "joao.silva@example.com")
        self.assertEqual(Professional.objects.get(id=1).phone, "2134567890")

        # Tear down
        professional.delete()

    def tearDown(self) -> None:
        Professional.objects.all().delete()
        self.business.delete()