# Generated by Django 4.2.11 on 2024-04-04 07:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='customer',
            unique_together={('first_name', 'last_name', 'dob')},
        ),
    ]
