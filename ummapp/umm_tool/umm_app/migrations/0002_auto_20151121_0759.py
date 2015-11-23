# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('umm_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='parent_quarter_id',
        ),
        migrations.AddField(
            model_name='category',
            name='parent_quarter_id',
            field=models.ForeignKey(default=1, to='umm_app.Quarter'),
            preserve_default=False,
        ),
    ]
