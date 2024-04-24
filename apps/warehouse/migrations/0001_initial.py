# Generated by Django 5.0.4 on 2024-04-24 08:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        ('purchase', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WarehouseProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0, verbose_name='quantity')),
                ('purchasing_amount', models.PositiveIntegerField(verbose_name='purchasing amount')),
                ('selling_amount', models.PositiveIntegerField(verbose_name='selling amount')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created time')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified time')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchase.provider')),
            ],
            options={
                'verbose_name': 'warehouse product',
                'verbose_name_plural': 'warehouse products',
                'db_table': 'warehouse_product',
                'ordering': ['-modified'],
            },
        ),
    ]
