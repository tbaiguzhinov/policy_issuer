from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, serializers
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView

from customers.models import Customer, Policy
from customers.serializers import (CustomerSerializer, PolicyCreateSerializer,
                                   PolicyListSeriazlier,
                                   PolicyUpdateSerializer)


class CustomerCreateView(CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


class QuoteView(GenericAPIView):
    queryset = Policy.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=PolicyCreateSerializer)
    def post(self, request, *args, **kwargs):
        serializer = PolicyCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)

    @swagger_auto_schema(request_body=PolicyUpdateSerializer)
    def patch(self, request, *args, **kwargs):
        serializer = PolicyUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)


class PolicyListView(ListAPIView):
    queryset = Policy.objects.all()
    serializer_class = PolicyListSeriazlier
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        customer_id = self.request.query_params.get('customer_id')
        try:
            Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            raise serializers.ValidationError('Customer not found')
        return Policy.objects.filter(customer=customer_id)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='customer_id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                required=True,
                description='Customer ID'
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)


class PolicyDetailView(GenericAPIView):
    queryset = Policy.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        policy_id = kwargs.get('policy_id')
        try:
            policy = Policy.objects.get(id=policy_id)
        except Policy.DoesNotExist:
            return JsonResponse(['Policy not found'], safe=False, status=400)
        serializer = PolicyListSeriazlier(policy)
        return JsonResponse(serializer.data, status=200)
