# Generated by Django 4.2.13 on 2024-07-03 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_alter_instagrammediacomment_hidden'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instagrammediadata',
            name='media_id',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
