# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('umm_app', '0002_auto_20151121_0759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='columndata',
            name='column_value',
            field=models.TextField(),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set([('category_name', 'parent_quarter_id')]),
        ),
    ]
