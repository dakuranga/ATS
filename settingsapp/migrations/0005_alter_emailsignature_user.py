# Generated by Django 4.2.7 on 2023-11-17 12:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('settingsapp', '0004_emailtemplate_templateattachment_emailsignature'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailsignature',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='settingsapp.tenantuser'),
        ),
    ]
