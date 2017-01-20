# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('umm_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubProcessLevelUpdates',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('data', models.TextField()),
                ('created_date', models.DateTimeField()),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(related_name='subprocessupdates_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(related_name='subprocessupdates_modified_by', to=settings.AUTH_USER_MODEL)),
                ('subprocess', models.ForeignKey(to='umm_app.SubProcess')),
            ],
        ),
    ]
