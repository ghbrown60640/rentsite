# Generated by Django 4.0b1 on 2021-11-10 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aptlist', '0011_auto_20201221_1913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='date_built',
            field=models.DateTimeField(verbose_name='date built'),
        ),
        migrations.AlterField(
            model_name='lease',
            name='lease_expires',
            field=models.DateTimeField(verbose_name='lease expires'),
        ),
    ]