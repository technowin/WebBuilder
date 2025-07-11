# Generated by Django 4.2.23 on 2025-07-09 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0009_websiteworkflow_enable_accessibility'),
    ]

    operations = [
        migrations.AddField(
            model_name='websiteworkflow',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='websiteworkflow',
            name='email_address',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='websiteworkflow',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
