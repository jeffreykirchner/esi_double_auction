# Generated by Django 3.2.2 on 2021-05-28 20:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_auto_20210526_1810'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parameterset',
            name='consent_form',
        ),
        migrations.RemoveField(
            model_name='parameterset',
            name='consent_form_required',
        ),
    ]
