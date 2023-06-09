# Generated by Django 4.2.1 on 2023-05-15 18:03

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.RunSQL(
            sql='CREATE SCHEMA IF NOT EXISTS billing;',
            reverse_sql='DROP SCHEMA IF EXISTS billing;'
        ),
        migrations.CreateModel(
            name='Consumer',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('id', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('user_id', models.UUIDField(null=True, verbose_name='ID пользователя')),
                ('email', models.EmailField(max_length=254, null=True, verbose_name='Email')),
                ('remote_consumer_id', models.CharField(blank=True, max_length=200, null=True, verbose_name='ID в платежной системе')),
            ],
            options={
                'verbose_name': 'Покупатель',
                'verbose_name_plural': 'Покупатели',
                'db_table': 'billing"."consumer',
            },
        ),
        migrations.CreateModel(
            name='Filmwork',
            fields=[
                ('id', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=200)),
                ('modified_subscribe_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Фильм',
                'verbose_name_plural': 'Фильмы',
                'db_table': 'billing"."filmwork',
            },
        ),
        migrations.CreateModel(
            name='Subscribe',
            fields=[
                ('id', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('subscribe_type', models.CharField(choices=[('SU', 'Наш кинотеатр'), ('AM', 'Амедиатека')], max_length=2, null=True, unique=True, verbose_name='Тип подписки')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Цена подписки USD')),
                ('payment_id', models.CharField(blank=True, max_length=200, null=True, verbose_name='ID продукта в платежной системе')),
            ],
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
                'db_table': 'billing"."subscribe',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('id', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Сумма покупки')),
                ('transaction_id', models.CharField(max_length=300)),
                ('consumer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='billing.consumer', verbose_name='Пользователь')),
                ('subscription', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='billing.subscribe', verbose_name='Подписка')),
            ],
            options={
                'verbose_name': 'Платеж',
                'verbose_name_plural': 'Платежи',
                'db_table': 'billing"."payment',
            },
        ),
        migrations.CreateModel(
            name='FilmworkSubscribe',
            fields=[
                ('id', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('filmwork', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='billing.filmwork')),
                ('subscribe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='billing.subscribe')),
            ],
            options={
                'verbose_name': 'Фильм в подписке',
                'verbose_name_plural': 'Фильмы в подписке',
                'db_table': 'billing"."filmwork_subscribe',
                'unique_together': {('filmwork', 'subscribe')},
            },
        ),
        migrations.AddField(
            model_name='filmwork',
            name='subscribe',
            field=models.ManyToManyField(through='billing.FilmworkSubscribe', to='billing.subscribe'),
        ),
        migrations.AddField(
            model_name='consumer',
            name='subscribe',
            field=models.ManyToManyField(blank=True, to='billing.subscribe', verbose_name='Подписки пользователя'),
        ),
        migrations.AddIndex(
            model_name='filmwork',
            index=models.Index(fields=['modified_subscribe_date'], name='filmwork_subscribe_date_idx'),
        ),
    ]
