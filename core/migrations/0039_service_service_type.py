# Generated by Django 4.2.13 on 2024-07-16 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_service_servicepricing'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='service_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
