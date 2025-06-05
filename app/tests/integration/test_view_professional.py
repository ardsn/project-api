from app.models import Professional, Business, City
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

class TestProfessionalView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        cls.city = City.objects.get(name="Ariquemes", state="RO")

        cls.business = Business.objects.create(
            name="Clínica Fagundes",
            category="C1",
            city=cls.city,
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

        cls.professional_args = {
            "name": "John Doe",
            "email": "email@example.com",
            "phone": "11 99595-4250",
            "business": cls.business,
            "cpf": "111.444.777-35",
            "speciality": "Dentista",
            "schedule": {
                "0": {
                    "start": "08:00",
                    "end": "17:00",
                    "breaks": []
                }
            }
        }
        
    def setUp(self):
        self.client.force_authenticate(user=self.user)

    def test_list_professionals(self):
        _ = Professional.objects.create(**self.professional_args)

        response = self.client.get(reverse('professional-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_list_professionals_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('professional-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_professional(self):
        professional = Professional.objects.create(**self.professional_args)
        response = self.client.get(
            reverse('professional-detail', args=[professional.id])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], professional.id)

    def test_get_professional_unauthenticated(self):
        self.client.force_authenticate(user=None)
        professional = Professional.objects.create(**self.professional_args)
        response = self.client.get(
            reverse('professional-detail', args=[professional.id])
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_professional(self):
        professional_data = self.professional_args | {"business": self.business.id}
        response = self.client.post(
            reverse('professional-list'),
            professional_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Professional.objects.count(), 1)

    def test_create_professional_unauthenticated(self):
        self.client.force_authenticate(user=None)
        professional_data = self.professional_args | {"business": self.business.id}
        response = self.client.post(
            reverse('professional-list'),
            professional_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_professional_with_invalid_field(self):
        professional_data = (
            self.professional_args
            |
            {
                "business": self.business.id,
                "phone": "(100) 4959-4250"
            }
        )

        response = self.client.post(
            reverse('professional-list'),
            professional_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_refuse_duplicate_professional(self):
        response = self.client.post(
            reverse('professional-list'),
            self.professional_args | {"business": self.business.id},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        professional_data = (
            self.professional_args
            |
            {
                "business": self.business.id,
                "email": "email2@example.com"
            }
        )

        response = self.client.post(
            reverse('professional-list'),
            professional_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_professional_field(self):
        professional = Professional.objects.create(**self.professional_args)
        updated_field = {"name": "Jane Doe"}

        response = self.client.patch(
            reverse('professional-detail', args=[professional.id]),
            updated_field,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Professional.objects.count(), 1)
        self.assertEqual(Professional.objects.get(id=professional.id).name, updated_field["name"])

    def test_update_professional_field_unauthenticated(self):
        self.client.force_authenticate(user=None)
        professional = Professional.objects.create(**self.professional_args)
        updated_field = {"name": "Jane Doe"}

        response = self.client.patch(
            reverse('professional-detail', args=[professional.id]),
            updated_field,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_professional(self):
        professional = Professional.objects.create(**self.professional_args)
        response = self.client.delete(
            reverse('professional-detail', args=[professional.id])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Professional.objects.count(), 0)

    def test_delete_professional_unauthenticated(self):
        self.client.force_authenticate(user=None)
        professional = Professional.objects.create(**self.professional_args)

        response = self.client.delete(
            reverse('professional-detail', args=[professional.id])
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        
    
        