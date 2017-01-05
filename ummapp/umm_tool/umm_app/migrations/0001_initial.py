# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email_pitch_guidelines', models.TextField()),
                ('implementation_guide', models.TextField()),
                ('faq', models.TextField()),
                ('elevator_pitch', models.TextField()),
                ('is_disable', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='BudgetBand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('band_details', models.TextField()),
                ('created_date', models.DateTimeField()),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category_name', models.CharField(unique=True, max_length=250)),
                ('created_date', models.DateTimeField()),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('is_disable', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ColumnData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('column_name', models.CharField(max_length=250)),
                ('column_value', models.TextField()),
                ('is_disable', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ComboUpdate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('created_date', models.DateTimeField()),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExtraTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('extra_task_name', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('goal_name', models.CharField(max_length=250)),
                ('created_date', models.DateField()),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('is_disable', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='GoalTaskMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateField()),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('is_disable', models.BooleanField(default=False)),
                ('parent_goal_id', models.ForeignKey(to='umm_app.Goal')),
            ],
        ),
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=250)),
                ('url_name', models.CharField(unique=True, max_length=250)),
                ('image_ref', models.ImageField(null=True, upload_to=b'processes/', blank=True)),
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
                ('name', models.CharField(max_length=250)),
                ('data', models.TextField()),
                ('created_date', models.DateTimeField()),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('is_disabled', models.BooleanField(default=False)),
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
                ('name', models.CharField(max_length=250)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('is_disabled', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(related_name='programtype_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(related_name='programtype_modified_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Quarter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quarter', models.IntegerField(default=1, choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4')])),
                ('quarter_year', models.IntegerField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.CharField(max_length=500)),
                ('parent_goal_id', models.ForeignKey(to='umm_app.Goal')),
            ],
        ),
        migrations.CreateModel(
            name='SubProcess',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('url_name', models.CharField(max_length=250)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('is_disabled', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(related_name='subprocess_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(related_name='subprocess_modified_by', to=settings.AUTH_USER_MODEL)),
                ('process', models.ForeignKey(to='umm_app.Process')),
                ('quarter', models.ForeignKey(to='umm_app.Quarter')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('task_name', models.CharField(max_length=250)),
                ('created_date', models.DateField()),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('is_disable', models.BooleanField(default=False)),
                ('parent_category_id', models.ForeignKey(to='umm_app.Category')),
            ],
        ),
        migrations.CreateModel(
            name='TaskData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('column_name', models.CharField(max_length=250)),
                ('column_number', models.IntegerField(default=0, null=True, blank=True)),
                ('data', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('is_disabled', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(related_name='taskdata_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(related_name='taskdata_modified_by', to=settings.AUTH_USER_MODEL)),
                ('program_task', models.ForeignKey(to='umm_app.ProgramTask')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='quarter',
            unique_together=set([('quarter', 'quarter_year')]),
        ),
        migrations.AddField(
            model_name='programtype',
            name='subprocess',
            field=models.ForeignKey(to='umm_app.SubProcess'),
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
            model_name='goaltaskmap',
            name='parent_task_id',
            field=models.ManyToManyField(to='umm_app.Task'),
        ),
        migrations.AddField(
            model_name='extratask',
            name='parent_goal_id',
            field=models.ForeignKey(to='umm_app.Goal'),
        ),
        migrations.AddField(
            model_name='comboupdate',
            name='parent_quarter_id',
            field=models.ForeignKey(to='umm_app.Quarter'),
        ),
        migrations.AddField(
            model_name='columndata',
            name='parent_task_id',
            field=models.ForeignKey(to='umm_app.Task'),
        ),
        migrations.AddField(
            model_name='category',
            name='parent_quarter_id',
            field=models.ForeignKey(to='umm_app.Quarter'),
        ),
        migrations.AddField(
            model_name='budgetband',
            name='parent_quarter_id',
            field=models.ForeignKey(to='umm_app.Quarter'),
        ),
        migrations.AddField(
            model_name='additiondata',
            name='parent_task_id',
            field=models.ForeignKey(to='umm_app.Task'),
        ),
        migrations.AlterUniqueTogether(
            name='taskdata',
            unique_together=set([('column_name', 'program_task')]),
        ),
        migrations.AlterUniqueTogether(
            name='task',
            unique_together=set([('task_name', 'parent_category_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='subprocess',
            unique_together=set([('process', 'name', 'quarter')]),
        ),
        migrations.AlterUniqueTogether(
            name='programtype',
            unique_together=set([('subprocess', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='programtask',
            unique_together=set([('name', 'program_type')]),
        ),
        migrations.AlterUniqueTogether(
            name='programadditiondata',
            unique_together=set([('program_task', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set([('category_name', 'parent_quarter_id')]),
        ),
    ]
