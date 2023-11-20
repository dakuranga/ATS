# Generated by Django 4.2.7 on 2023-11-11 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('code', models.CharField(max_length=200)),
                ('website', models.URLField(max_length=255)),
                ('about_client_attachment', models.FileField(upload_to='Clients/')),
                ('hq', models.CharField(blank=True, max_length=200, null=True)),
                ('industry', models.CharField(max_length=200)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
