# Generated by Django 4.2.7 on 2023-11-16 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_alter_job_job_harvestor_string'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='job_code',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]