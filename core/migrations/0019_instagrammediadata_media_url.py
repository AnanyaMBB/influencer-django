# Generated by Django 4.2.13 on 2024-07-02 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_alter_instagrammediadata_is_comment_enabled_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='instagrammediadata',
            name='media_url',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
