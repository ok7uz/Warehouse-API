# Generated by Django 5.0.3 on 2024-05-05 11:36

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('warehouse', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cash',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Cashier',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('cach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cashiers', to='cash.cash')),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.FloatField()),
                ('cash', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='cash.cash')),
                ('cashier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='cash.cashier')),
            ],
        ),
        migrations.CreateModel(
            name='SaleProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sale_products', to='warehouse.warehouseproduct')),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='cash.sale')),
            ],
        ),
    ]
