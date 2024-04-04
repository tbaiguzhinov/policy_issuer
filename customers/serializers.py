from rest_framework import serializers

from customers.models import Customer, Policy


class CustomerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'dob']


class PolicySerializer(serializers.ModelSerializer):
    policy_number = serializers.UUIDField(read_only=True)
    state = serializers.CharField(read_only=True)

    class Meta:
        model = Policy
        fields = [
            'policy_number',
            'type',
            'premium',
            'cover',
            'state',
            'customer'
        ]
