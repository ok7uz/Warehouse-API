# Generated by Django 5.0.3 on 2024-05-05 19:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0001_initial'),
        ('warehouse', '0002_warehouseproduct_is_avaiable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase_products', to='warehouse.warehouseproduct'),
        ),
    ]
