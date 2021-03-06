# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-13 10:18
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('backbone', '0005_auto_20170212_1631'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('card', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.TextField()),
                ('transaction_id', models.TextField()),
                ('destination_name', models.TextField()),
                ('destination_country', models.TextField()),
                ('destination_mcc', models.TextField()),
                ('billing_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('billing_currency', models.TextField()),
                ('transaction_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transaction_currency', models.TextField()),
                ('settelment_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('settelment_currency', models.TextField()),
                ('date', models.DateTimeField(default=datetime.datetime(2017, 2, 13, 10, 18, 13, 421816, tzinfo=utc))),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backbone.Accounts')),
            ],
        ),
        migrations.CreateModel(
            name='Transfers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('debit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('credit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField()),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backbone.Accounts')),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backbone.Transactions')),
            ],
        ),
        migrations.RemoveField(
            model_name='operation',
            name='account',
        ),
        migrations.RemoveField(
            model_name='operation',
            name='transaction',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='source',
        ),
        migrations.DeleteModel(
            name='Operation',
        ),
        migrations.DeleteModel(
            name='Transaction',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
