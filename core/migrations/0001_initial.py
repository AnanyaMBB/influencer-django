# Generated by Django 4.2.13 on 2024-06-18 19:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('company_name', models.CharField(blank=True, max_length=100, null=True)),
                ('company_industry', models.CharField(blank=True, max_length=100, null=True)),
                ('company_website', models.CharField(blank=True, max_length=100, null=True)),
                ('company_size', models.IntegerField(blank=True, null=True)),
                ('company_email', models.CharField(blank=True, max_length=100, null=True)),
                ('company_address', models.CharField(blank=True, max_length=100, null=True)),
                ('company_phone', models.CharField(blank=True, max_length=100, null=True)),
                ('company_city', models.CharField(blank=True, max_length=100, null=True)),
                ('company_state', models.CharField(blank=True, max_length=100, null=True)),
                ('company_zip', models.CharField(blank=True, max_length=100, null=True)),
                ('company_country', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
