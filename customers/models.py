from django.db import models
from simple_history.models import HistoricalRecords

from customers.constants import PolicyStateChoices


class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['first_name', 'last_name', 'dob']

    def __str__(self):
        if self.last_name:
            return f'{self.first_name} {self.last_name}'
        return self.first_name


class Policy(models.Model):
    type = models.CharField(max_length=100)
    premium = models.IntegerField()
    cover = models.IntegerField()
    state = models.CharField(
        max_length=100,
        choices=PolicyStateChoices.CHOICES,
        default=PolicyStateChoices.NEW
    )
    history = HistoricalRecords()

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='policies',
        null=True,
    )

    policy_start_date = models.DateField(null=True, blank=True)
    policy_end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Policies'
        unique_together = ['type', 'customer', 'premium', 'cover']

    def __str__(self):
        return str(self.id)
