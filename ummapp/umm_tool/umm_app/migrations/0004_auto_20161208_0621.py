# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('umm_app', '0003_auto_20161207_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='process',
            name='image_ref',
            field=models.ImageField(null=True, upload_to=b'processes/', blank=True),
        ),
    ]
