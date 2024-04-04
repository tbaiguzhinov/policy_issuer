from django.contrib import admin

from customers.models import Customer, Policy


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'dob', 'created_at']
    search_fields = ['first_name', 'last_name']


@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = [
        'policy_number',
        'type',
        'premium',
        'cover',
        'state',
        'customer',
        'created_at'
    ]
    search_fields = ['policy_number', 'type']
