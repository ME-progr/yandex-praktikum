# Generated by Django 4.2 on 2023-04-20 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notify', '0003_notifytype_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='notify',
            name='retry_count',
            field=models.IntegerField(default=0, verbose_name='Попыток отправки'),
        ),
    ]
