# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-13 11:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backbone', '0007_auto_20170213_1157'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactions',
            name='date',
        ),
    ]
