# Generated by Django 2.2.11 on 2020-04-05 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discount', '0005_auto_20200405_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='period',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Act', 'Active'), ('Rec', 'Reconciliation'), ('Clo', 'Closed')], max_length=32),
        ),
    ]
