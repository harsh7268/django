# Generated by Django 4.1.3 on 2022-11-11 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_booking_payment_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='gallary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('galary_pic', models.ImageField(blank=True, null=True, upload_to='Galary')),
            ],
        ),
    ]