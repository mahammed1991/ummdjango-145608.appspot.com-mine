# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('umm_app', '0002_auto_20161206_0607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='process',
            name='image_ref',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
    ]
