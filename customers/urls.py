from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from customers import views

schema_view = get_schema_view(
   openapi.Info(
      title="Policy Issuer API",
      default_version='v1',
      description="API for Policy creation service",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="tim.baiguzhinov@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
    path(
        'create_customer/',
        views.CustomerCreateView.as_view(),
        name='customer-create'
    ),
    # path(
    #     'customers/<int:pk>/',
    #     views.CustomerDetail.as_view(),
    #     name='customer-detail'
    # ),
]