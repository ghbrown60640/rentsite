# Generated by Django 3.1.4 on 2020-12-20 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aptlist', '0004_auto_20201219_0029'),
    ]

    operations = [
        migrations.AddField(
            model_name='lease',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
