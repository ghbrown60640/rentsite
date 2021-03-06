# Generated by Django 3.1.4 on 2020-12-21 19:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('aptlist', '0009_auto_20201221_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='date_built',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date built'),
        ),
        migrations.AlterField(
            model_name='lease',
            name='lease_expires',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='lease expires'),
        ),
    ]
