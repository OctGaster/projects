# Generated by Django 2.2.11 on 2020-03-31 15:31

import discount.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agreement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(verbose_name='date of the start')),
                ('stop_date', models.DateTimeField(verbose_name='date of the stop')),
                ('debit', models.IntegerField(default=0)),
                ('credit', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(verbose_name='date of the start')),
                ('stop_date', models.DateTimeField(verbose_name='date of the stop')),
                ('status', models.CharField(choices=[(discount.models.Status('New'), 'New'), (discount.models.Status('Active'), 'Active'), (discount.models.Status('Reconciliation'), 'Reconciliation'), (discount.models.Status('Closed'), 'Closed')], max_length=3)),
                ('agreement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discount.Agreement')),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discount.Country')),
            ],
        ),
        migrations.AddField(
            model_name='agreement',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discount.Company'),
        ),
        migrations.AddField(
            model_name='agreement',
            name='negotiator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
