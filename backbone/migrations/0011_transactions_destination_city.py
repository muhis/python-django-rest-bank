# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-13 18:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backbone', '0010_auto_20170213_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='destination_city',
            field=models.TextField(null=True),
        ),
    ]
