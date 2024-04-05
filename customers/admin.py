from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from customers.models import Customer, Policy


class PolicyInline(admin.TabularInline):
    model = Policy
    extra = 0
    readonly_fields = ['created_at']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'dob', 'created_at']
    search_fields = ['first_name', 'last_name', 'dob', 'policies__type']
    inlines = [PolicyInline]


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
    readonly_fields = ['created_at']
    search_fields = ['type', 'customer__first_name', 'customer__last_name']
    list_filter = ['state']
