# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('umm_app', '0003_auto_20170105_0638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subprocesslevelupdates',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
