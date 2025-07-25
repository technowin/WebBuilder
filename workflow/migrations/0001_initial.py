# Generated by Django 4.2.23 on 2025-07-03 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WebsiteCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('category_name', models.TextField(blank=True, null=True)),
                ('is_active', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.CharField(blank=True, max_length=100, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('updated_by', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'tbl_websiteCategoryMaster',
            },
        ),
    ]
