# Generated by Django 4.2.7 on 2023-11-17 09:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('settingsapp', '0002_tenantuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useremail',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='settingsapp.tenantuser'),
        ),
    ]
