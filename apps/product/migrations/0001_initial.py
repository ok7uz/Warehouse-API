# Generated by Django 5.0.4 on 2024-04-24 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('barcode', models.PositiveIntegerField(verbose_name='barcode')),
                ('id_code', models.PositiveIntegerField(verbose_name='ID code')),
                ('currency', models.CharField(choices=[('UZS', 'UZS'), ('USD', 'USD')], max_length=3,
                                              verbose_name='currency')),
                ('purchasing_price', models.FloatField(verbose_name='purchasing price')),
                ('markup_percentage', models.PositiveSmallIntegerField(verbose_name='markup percentage')),
                ('selling_price', models.FloatField(verbose_name='selling price')),
                ('wholesale_price', models.FloatField(verbose_name='wholesale price')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created time')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified time')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'db_table': 'product',
                'ordering': ['-modified'],
            },
        ),
    ]
