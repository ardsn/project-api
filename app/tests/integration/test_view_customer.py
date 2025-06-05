from app.models import Business, City, Customer
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class TestCustomerView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        cls.business = Business.objects.create(
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
        cls.customer_args = {
            "business": cls.business,
            "name": "Test Customer",
            "registration_source": "WEBSITE",
            "cpf": "111.444.777-35",
            "email": "test@example.com",
            "phone": "11995954250"
        }

    def setUp(self):
        self.client.force_authenticate(user=self.user)

    def test_list_customers(self):
        _ = Customer.objects.create(**self.customer_args)
        response = self.client.get(reverse('customer-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_list_customers_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('customer-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_customer(self):
        customer = Customer.objects.create(**self.customer_args)
        response = self.client.get(
            reverse('customer-detail', args=[customer.id])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], customer.id)

    def test_get_customer_unauthenticated(self):
        self.client.force_authenticate(user=None)
        customer = Customer.objects.create(**self.customer_args)
        response = self.client.get(
            reverse('customer-detail', args=[customer.id])
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_customer(self):
        customer_data = self.customer_args | {"business": self.business.id}
        response = self.client.post(
            reverse('customer-list'),
            customer_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 1)

    def test_create_customer_unauthenticated(self):
        self.client.force_authenticate(user=None)
        customer_data = self.customer_args | {"business": self.business.id}
        response = self.client.post(
            reverse('customer-list'),
            customer_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_customer_with_invalid_field(self):
        customer_data = self.customer_args | {"business": self.business.id, "cpf": "123.456.789-00"}
        response = self.client.post(
            reverse('customer-list'),
            customer_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_refuse_duplicate_customer(self):
        response = self.client.post(
            reverse('customer-list'),
            self.customer_args | {"business": self.business.id},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        customer_data = (
            self.customer_args
            |
            {
                "business": self.business.id,
                "email": "test2@example.com",
                "phone": "(89) 99595-4250"
            }
        )

        response = self.client.post(
            reverse('customer-list'),
            customer_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_customer_field(self):
        customer = Customer.objects.create(**self.customer_args)
        updated_field = {"name": "Test Customer 2"}

        response = self.client.patch(
            reverse('customer-detail', args=[customer.id]),
            updated_field,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Customer.objects.get(id=customer.id).name, updated_field["name"])

    def test_update_customer_field_unauthenticated(self):
        self.client.force_authenticate(user=None)
        customer = Customer.objects.create(**self.customer_args)
        updated_field = {"name": "Test Customer 2"}

        response = self.client.patch(
            reverse('customer-detail', args=[customer.id]),
            updated_field,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_customer(self):
        customer = Customer.objects.create(**self.customer_args)
        response = self.client.delete(
            reverse('customer-detail', args=[customer.id])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Customer.objects.count(), 0)

    def test_delete_customer_unauthenticated(self):
        self.client.force_authenticate(user=None)
        customer = Customer.objects.create(**self.customer_args)

        response = self.client.delete(
            reverse('customer-detail', args=[customer.id])
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
