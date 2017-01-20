# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('umm_app', '0004_auto_20170105_0940'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgramAdditionData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('data', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('is_disabled', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(related_name='adddata_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(related_name='adddata_modified_by', to=settings.AUTH_USER_MODEL)),
                ('program_task', models.ForeignKey(to='umm_app.ProgramTask')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='programadditiondata',
            unique_together=set([('program_task', 'name')]),
        ),
    ]
