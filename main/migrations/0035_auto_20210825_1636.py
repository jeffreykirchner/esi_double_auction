# Generated by Django 3.2.6 on 2021-08-25 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0034_auto_20210813_0006'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='locked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='session',
            name='shared',
            field=models.BooleanField(default=False),
        ),
    ]
