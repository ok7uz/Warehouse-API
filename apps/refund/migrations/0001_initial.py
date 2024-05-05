# Generated by Django 5.0.3 on 2024-05-05 05:57

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
            name='Refund',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.CharField(max_length=256, verbose_name='created time')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('invoice_number', models.PositiveIntegerField()),
                ('currency', models.CharField(choices=[('UZS', 'UZS'), ('USD', 'USD')], max_length=3, verbose_name='currency')),
                ('amount', models.FloatField()),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='refunds', to='warehouse.provider')),
            ],
            options={
                'verbose_name': 'refund',
                'verbose_name_plural': 'refund',
                'db_table': 'refund',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='RefundProduct',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('total', models.FloatField()),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created time')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified time')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.warehouseproduct')),
                ('refund', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='refund.refund')),
            ],
            options={
                'verbose_name': 'refund product',
                'verbose_name_plural': 'refund products',
                'db_table': 'refund_product',
                'ordering': ['-modified'],
            },
        ),
    ]