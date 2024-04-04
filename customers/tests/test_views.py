from datetime import date

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from customers.models import Customer, Policy
from customers.serializers import CustomerSerializer, PolicySerializer


class CustomerCreateViewTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='adminpassword'
        )
        self.client.force_login(self.admin_user)

    def test_create_customer(self):
        url = reverse('customer-create')
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'dob': '01-01-1990'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 1)
        customer = Customer.objects.get()
        self.assertEqual(customer.first_name, 'John')
        self.assertEqual(customer.last_name, 'Doe')
        self.assertEqual(customer.dob, date(1990, 1, 1))
        self.assertEqual(
            response.data,
            CustomerSerializer(Customer.objects.get()).data
        )


class QuoteCreateViewTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='adminpassword'
        )
        self.client.force_login(self.admin_user)
        self.customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            dob=date(1990, 1, 1)
        )

    def test_create_quote(self):
        url = reverse('quote-create')
        data = {
            'customer': self.customer.id,
            'type': 'life',
            'premium': 100,
            'cover': 100000,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Policy.objects.count(), 1)
        self.assertEqual(
            self.customer.policies.count(),
            1
        )
