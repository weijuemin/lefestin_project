# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-29 03:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lefestin', '0004_auto_20160728_2048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='creator',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='lefestin.User'),
        ),
    ]