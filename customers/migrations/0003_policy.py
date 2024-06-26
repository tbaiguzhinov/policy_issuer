# Generated by Django 4.2.11 on 2024-04-04 09:40

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_alter_customer_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('premium', models.IntegerField()),
                ('cover', models.IntegerField()),
                ('state', models.CharField(choices=[('new', 'New'), ('quoted', 'Quoted'), ('active', 'Active')], default='new', max_length=100)),
                ('policy_start_date', models.DateField(blank=True, null=True)),
                ('policy_end_date', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.customer')),
            ],
        ),
    ]
