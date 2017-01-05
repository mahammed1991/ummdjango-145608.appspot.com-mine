# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('umm_app', '0002_subprocesslevelupdates'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='subprocesslevelupdates',
            unique_together=set([('subprocess', 'name')]),
        ),
    ]
