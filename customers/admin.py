from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from customers.models import Customer, Policy


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'dob', 'created_at']
    search_fields = ['first_name', 'last_name']


@admin.register(Policy)
class PolicyAdmin(SimpleHistoryAdmin):
    list_display = [
        'id',
        'type',
        'premium',
        'cover',
        'state',
        'customer',
        'created_at',
    ]
    search_fields = ['id', 'type']
