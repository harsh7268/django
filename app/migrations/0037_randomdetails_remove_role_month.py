# Generated by Django 4.1.7 on 2023-04-29 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0036_remove_notification_month_role_month'),
    ]

    operations = [
        migrations.CreateModel(
            name='RandomDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='role',
            name='month',
        ),
    ]
