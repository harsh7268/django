# Generated by Django 4.1.7 on 2023-04-29 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0032_attendancepdfform_mem_id_attendancepdfform_mem_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendancepdfform',
            name='is_uploaded',
            field=models.BooleanField(default=False),
        ),
    ]