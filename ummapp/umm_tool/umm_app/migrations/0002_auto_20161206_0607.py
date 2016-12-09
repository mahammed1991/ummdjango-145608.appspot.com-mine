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
            name='AdditionDataReference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('is_disabled', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(related_name='dataref_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(related_name='dataref_modified_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=250)),
                ('url_name', models.CharField(unique=True, max_length=250)),
                ('image_ref', models.CharField(max_length=20)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('is_disabled', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(related_name='process_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(related_name='process_modified_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProgramAdditionData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.TextField()),
                ('created_date', models.DateTimeField()),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('is_disabled', models.BooleanField(default=False)),
                ('additional_ref', models.ForeignKey(to='umm_app.AdditionDataReference')),
                ('created_by', models.ForeignKey(related_name='adddata_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(related_name='adddata_modified_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProgramTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('is_disabled', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(related_name='programtask_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(related_name='programtask_modified_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProgramType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=250)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('is_disabled', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(related_name='programtype_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(related_name='programtype_modified_by', to=settings.AUTH_USER_MODEL)),
                ('process', models.ForeignKey(to='umm_app.Process')),
                ('quarter', models.ForeignKey(to='umm_app.Quarter')),
            ],
        ),
        migrations.CreateModel(
            name='TaskData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('column_name', models.CharField(max_length=250)),
                ('data', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('is_disabled', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(related_name='taskdata_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(related_name='taskdata_modified_by', to=settings.AUTH_USER_MODEL)),
                ('program_task', models.ForeignKey(to='umm_app.ProgramTask')),
            ],
        ),
        migrations.AddField(
            model_name='programtask',
            name='program_type',
            field=models.ForeignKey(to='umm_app.ProgramType'),
        ),
        migrations.AddField(
            model_name='programadditiondata',
            name='program_task',
            field=models.ForeignKey(to='umm_app.ProgramTask'),
        ),
        migrations.AddField(
            model_name='programadditiondata',
            name='quarter',
            field=models.ForeignKey(to='umm_app.Quarter'),
        ),
        migrations.AlterUniqueTogether(
            name='programtype',
            unique_together=set([('process', 'name', 'quarter')]),
        ),
        migrations.AlterUniqueTogether(
            name='programtask',
            unique_together=set([('name', 'program_type')]),
        ),
        migrations.AlterUniqueTogether(
            name='programadditiondata',
            unique_together=set([('program_task', 'additional_ref', 'quarter')]),
        ),
    ]
