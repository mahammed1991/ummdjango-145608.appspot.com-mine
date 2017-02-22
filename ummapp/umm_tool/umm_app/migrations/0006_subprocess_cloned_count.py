# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('umm_app', '0005_auto_20170106_0657'),
    ]

    operations = [
        migrations.AddField(
            model_name='subprocess',
            name='cloned_count',
            field=models.IntegerField(default=0),
        ),
    ]
