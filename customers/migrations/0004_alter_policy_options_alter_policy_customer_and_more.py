# Generated by Django 4.1 on 2024-04-04 09:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_policy'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='policy',
            options={'verbose_name_plural': 'Policies'},
        ),
        migrations.AlterField(
            model_name='policy',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='policies', to='customers.customer'),
        ),
        migrations.AlterUniqueTogether(
            name='policy',
            unique_together={('type', 'customer', 'premium', 'cover')},
        ),
    ]
