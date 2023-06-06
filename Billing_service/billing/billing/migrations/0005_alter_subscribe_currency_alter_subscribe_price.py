# Generated by Django 4.2.1 on 2023-05-16 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0004_subscribe_currency_subscribe_interval'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscribe',
            name='currency',
            field=models.CharField(choices=[('usd', 'USD')], max_length=5, null=True, verbose_name='Тип валюты'),
        ),
        migrations.AlterField(
            model_name='subscribe',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Цена подписки'),
        ),
    ]