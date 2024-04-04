from rest_framework import permissions
from rest_framework.generics import CreateAPIView

from customers.models import Customer, Policy
from customers.serializers import CustomerSerializer, PolicySerializer


class CustomerCreateView(CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


class QuoteCreateView(CreateAPIView):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()
