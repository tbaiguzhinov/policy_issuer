from django.utils import timezone
from rest_framework import serializers

from customers.constants import POLICY_DURATION_DAYS
from customers.models import Customer, Policy


class CustomDateFormatField(serializers.DateField):
    def to_representation(self, value):
        return value.strftime('%m-%d-%Y')


class CustomerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    dob = CustomDateFormatField(format='%m-%d-%Y', input_formats=['%m-%d-%Y'])

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'dob']


class PolicyCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    state = serializers.CharField(read_only=True)
    customer_id = serializers.IntegerField(required=True)

    def validate(self, attrs):
        customer_id = attrs.get('customer_id')
        try:
            Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            raise serializers.ValidationError('Customer not found')
        return super().validate(attrs)

    class Meta:
        model = Policy
        fields = [
            'id',
            'type',
            'premium',
            'cover',
            'state',
            'customer_id'
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
            'customer_id',
            'policy_start_date',
            'policy_end_date',
        ]


class PolicyHistorySeriazlier(serializers.ModelSerializer):
    order_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Policy
        fields = [
            'order_id',
            'history',
        ]
