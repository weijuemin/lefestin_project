# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-29 03:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lefestin', '0005_auto_20160728_2050'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='creator',
        ),
    ]