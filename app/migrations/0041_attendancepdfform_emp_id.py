# Generated by Django 4.1.7 on 2023-05-08 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0040_notification_emp_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendancepdfform',
            name='emp_id',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
