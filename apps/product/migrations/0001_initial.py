# Generated by Django 5.0.3 on 2024-05-05 05:57

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
                ('currency', models.CharField(choices=[('UZS', 'UZS'), ('USD', 'USD')], max_length=3, verbose_name='currency')),
                ('purchasing_price', models.FloatField(verbose_name='purchasing price')),
                ('markup_percentage', models.FloatField(verbose_name='markup percentage')),
                ('selling_price', models.FloatField(verbose_name='selling price')),
                ('wholesale_price', models.FloatField(blank=True, null=True, verbose_name='wholesale price')),
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
