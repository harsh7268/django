# Generated by Django 4.1.7 on 2023-04-28 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0031_alter_attendancepdfform_pdf_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendancepdfform',
            name='mem_id',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='attendancepdfform',
            name='mem_name',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
