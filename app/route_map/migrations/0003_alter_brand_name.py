# Generated by Django 4.0 on 2023-11-20 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('route_map', '0002_brand_inventorylocation_job_repair_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='name',
            field=models.CharField(max_length=40),
        ),
    ]
