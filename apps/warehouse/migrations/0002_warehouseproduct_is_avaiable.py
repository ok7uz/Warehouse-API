# Generated by Django 5.0.3 on 2024-05-05 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='warehouseproduct',
            name='is_avaiable',
            field=models.BooleanField(default=True),
        ),
    ]