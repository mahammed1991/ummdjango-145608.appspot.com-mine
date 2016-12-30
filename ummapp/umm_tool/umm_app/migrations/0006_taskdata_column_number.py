# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('umm_app', '0005_auto_20161229_0937'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskdata',
            name='column_number',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
    ]
