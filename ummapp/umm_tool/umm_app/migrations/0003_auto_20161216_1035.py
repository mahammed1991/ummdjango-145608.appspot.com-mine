# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('umm_app', '0002_auto_20161214_0801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quarter',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
