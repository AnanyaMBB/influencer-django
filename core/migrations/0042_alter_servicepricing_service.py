# Generated by Django 4.2.13 on 2024-07-16 22:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0041_alter_servicepricing_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicepricing',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.service'),
        ),
    ]
