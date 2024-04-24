# Generated by Django 5.0.3 on 2024-04-24 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='markup_percentage',
            field=models.FloatField(verbose_name='markup percentage'),
        ),
        migrations.AlterField(
            model_name='product',
            name='wholesale_price',
            field=models.FloatField(blank=True, null=True, verbose_name='wholesale price'),
        ),
    ]
