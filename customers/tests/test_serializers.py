from datetime import date

from django.test import TestCase
from rest_framework.exceptions import ErrorDetail

from customers.models import Customer
from customers.serializers import PolicyCreateSerializer


class PolicyCreateSerializerTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            dob=date(1990, 1, 1)
        )

    def test_valid_data(self):
        serializer = PolicyCreateSerializer(data={
            'type': 'Life',
            'premium': 100,
            'cover': 100000,
            'customer_id': self.customer.id
        })
        self.assertTrue(serializer.is_valid())
        policy = serializer.save()
        self.assertEqual(policy.type, 'Life')
        self.assertEqual(policy.premium, 100)
        self.assertEqual(policy.cover, 100000)
        self.assertEqual(policy.state, 'new')
        self.assertEqual(policy.customer, self.customer)

    def test_invalid_customer_id(self):
        serializer = PolicyCreateSerializer(data={
            'type': 'Life',
            'premium': 100,
            'cover': 100000,
            'customer_id': 999  # Non-existent customer ID
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors,
            {'non_field_errors': [
                ErrorDetail(string='Customer not found', code='invalid')
            ]}
        )

    def test_missing_customer_id(self):
        serializer = PolicyCreateSerializer(data={
            'type': 'Life',
            'premium': 100,
            'cover': 100000
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors,
            {'customer_id': ['This field is required.']}
        )
