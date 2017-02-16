# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('umm_app', '0007_qualityframework'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qualityframework',
            name='name',
            field=models.CharField(unique=True, max_length=250),
        ),
    ]
