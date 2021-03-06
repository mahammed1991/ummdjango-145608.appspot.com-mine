# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('umm_app', '0006_subprocess_cloned_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.TextField()),
                ('answer', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(related_name='faq_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(related_name='faq_modified_by', to=settings.AUTH_USER_MODEL)),
                ('program_task', models.ForeignKey(blank=True, to='umm_app.ProgramTask', null=True)),
                ('program_type', models.ForeignKey(blank=True, to='umm_app.ProgramType', null=True)),
            ],
        ),
    ]
