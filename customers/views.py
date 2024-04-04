from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, GenericAPIView

from customers.models import Customer, Policy
from customers.serializers import (CustomerSerializer, PolicyCreateSerializer,
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
