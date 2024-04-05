from datetime import date, datetime

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from customers.models import Customer, Policy
from customers.serializers import CustomerSerializer, PolicyListSeriazlier


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
        url = reverse('quote-create-update')
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

    def test_create_quote_invalid(self):
        url = reverse('quote-create-update')
        data = {
            'customer': self.customer.id,
            'premium': 100,
            'cover': 100000,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {'type': ['This field is required.']}
        )


class QuoteUpdateViewTest(APITestCase):

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
        self.policy = Policy.objects.create(
            customer=self.customer,
            type='life',
            premium=100,
            cover=100000
        )

    def test_update_quote(self):
        url = reverse('quote-create-update')
        data = {
            'quote_id': self.policy.id,
            'state': 'active'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.policy.refresh_from_db()
        self.assertEqual(self.policy.state, 'active')

    def test_update_quote_invalid(self):
        url = reverse('quote-create-update')
        data = {
            'quote_id': self.policy.id,
            'state': 'invalid'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {'state': ['"invalid" is not a valid choice.']}
        )

    def test_update_quote_missing(self):
        url = reverse('quote-create-update')
        data = {
            'quote_id': 999,
            'state': 'active'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), ['Policy not found'])


class PolicyListViewTest(APITestCase):

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
        self.policy = Policy.objects.create(
            customer=self.customer,
            type='life',
            premium=100,
            cover=100000
        )

    def test_get_policy_list(self):
        url = reverse('policy-list')
        response = self.client.get(url, {'customer_id': self.customer.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = PolicyListSeriazlier(self.policy)
        self.assertEqual(response.json(), [serializer.data])

    def test_get_policy_list_invalid_customer(self):
        url = reverse('policy-list')
        response = self.client.get(url, {'customer_id': 999})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), ['Customer not found'])


class PolicyDetailViewTest(APITestCase):

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
        self.policy = Policy.objects.create(
            customer=self.customer,
            type='life',
            premium=100,
            cover=100000
        )

    def test_get_policy_detail(self):
        url = reverse('policy-detail', kwargs={'policy_id': self.policy.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = PolicyListSeriazlier(self.policy)
        self.assertEqual(response.json(), serializer.data)

    def test_get_policy_detail_invalid(self):
        url = reverse('policy-detail', kwargs={'policy_id': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), ['Policy not found'])


class PolicyHistoryViewTest(APITestCase):

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
        self.policy = Policy.objects.create(
            customer=self.customer,
            type='life',
            premium=100,
            cover=100000
        )

    def test_get_policy_history(self):
        url = reverse('policy-history', kwargs={'policy_id': self.policy.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        history_entry = response.json()[0]
        self.assertEqual(history_entry['state'], self.policy.state)
        self.assertEqual(
            datetime.strptime(
                history_entry['changed_at'],
                '%Y-%m-%dT%H:%M:%S.%fZ'
            ).date(),
            self.policy.history.first().history_date.date()
        )
        self.assertEqual(history_entry['user'], 'System')

    def test_get_policy_history_multiple(self):
        url = reverse('quote-create-update')
        data = {
            'quote_id': self.policy.id,
            'state': 'accepted'
        }
        self.client.patch(url, data, format='json')

        url = reverse('policy-history', kwargs={'policy_id': self.policy.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)
        history_entry = response.json()[-1]
        self.assertEqual(history_entry['state'], 'accepted')

    def test_get_policy_history_invalid(self):
        url = reverse('policy-history', kwargs={'policy_id': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), ['Policy not found'])
