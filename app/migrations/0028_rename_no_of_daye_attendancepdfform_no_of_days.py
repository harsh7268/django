# Generated by Django 4.1.7 on 2023-04-26 06:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_remove_attendancepdfform_mem_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendancepdfform',
            old_name='no_of_daye',
            new_name='no_of_days',
        ),
    ]