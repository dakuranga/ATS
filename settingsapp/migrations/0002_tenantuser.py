# Generated by Django 4.2.7 on 2023-11-17 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settingsapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TenantUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('is_active', models.BooleanField(default=False)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
            ],
        ),
    ]
