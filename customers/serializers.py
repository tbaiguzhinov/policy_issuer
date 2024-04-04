from django.utils import timezone
from rest_framework import serializers

from customers.constants import POLICY_DURATION_DAYS
from customers.models import Customer, Policy


class CustomerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'dob']


class PolicyCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    state = serializers.CharField(read_only=True)

    class Meta:
        model = Policy
        fields = [
            'id',
            'type',
            'premium',
            'cover',
            'state',
            'customer'
        ]


class PolicyUpdateSerializer(serializers.ModelSerializer):
    quote_id = serializers.IntegerField()

    def update(self):
        quote_id = self.validated_data.get('quote_id')
        try:
            instance = Policy.objects.get(id=quote_id)
        except Policy.DoesNotExist:
            raise serializers.ValidationError('Policy not found')
        instance.state = self.validated_data.get('state', instance.state)
        if instance.state == 'active':
            instance.policy_start_date = timezone.now()
            instance.policy_end_date = instance.policy_start_date \
                + timezone.timedelta(days=POLICY_DURATION_DAYS)
        instance.save()
        return instance

    class Meta:
        model = Policy
        fields = [
            'quote_id',
            'state',
        ]


class PolicyListSeriazlier(serializers.ModelSerializer):
    customer_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Policy
        fields = [
            'id',
            'type',
            'premium',
            'cover',
            'state',
            'customer',
            'customer_id'
        ]
