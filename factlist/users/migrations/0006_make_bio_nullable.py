# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-05-08 11:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_name_and_bio_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.CharField(blank=True, max_length=160, null=True),
        ),
    ]