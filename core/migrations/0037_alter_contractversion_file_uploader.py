# Generated by Django 4.2.13 on 2024-07-14 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_contract_influencerinstagraminformation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractversion',
            name='file_uploader',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
