# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('umm_app', '0004_auto_20161227_0718'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='taskdata',
            unique_together=set([('column_name', 'program_task')]),
        ),
    ]
