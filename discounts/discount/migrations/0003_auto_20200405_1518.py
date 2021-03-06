# Generated by Django 2.2.11 on 2020-04-05 15:18

import discount.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discount', '0002_auto_20200404_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='period',
            name='status',
            field=models.CharField(choices=[(discount.models.Status('New'), 'New'), (discount.models.Status('Active'), 'Active'), (discount.models.Status('Reconciliation'), 'Reconciliation'), (discount.models.Status('Closed'), 'Closed')], max_length=32),
        ),
    ]
