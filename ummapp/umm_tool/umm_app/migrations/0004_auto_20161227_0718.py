# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('umm_app', '0003_auto_20161216_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programtype',
            name='name',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='subprocess',
            name='name',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='subprocess',
            name='url_name',
            field=models.CharField(max_length=250),
        ),
    ]
