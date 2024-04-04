from datetime import date

from django.test import TestCase

from customers.models import Customer


class CustomerModelTest(TestCase):
    def setUp(self):
        self.customer1 = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            dob=date(1990, 1, 1)
        )

    def test_customer_str_representation(self):
        self.assertEqual(str(self.customer1), 'John Doe')

    def test_customer_blank_last_name(self):
        customer = Customer.objects.create(
            first_name='Jane',
            dob=date(1995, 5, 5)
        )
        self.assertEqual(str(customer), 'Jane')

    def test_customer_created_at_auto_now_add(self):
        customer = Customer.objects.create(
            first_name='Alice',
            last_name='Smith',
            dob=date(1985, 12, 31)
        )
        self.assertIsNotNone(customer.created_at)
