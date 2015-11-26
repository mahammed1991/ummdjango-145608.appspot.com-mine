# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email_pitch_guidelines', models.CharField(max_length=250)),
                ('implementation_guide', models.CharField(max_length=250)),
                ('faq', models.CharField(max_length=250)),
                ('elevator_pitch', models.TextField(max_length=1000)),
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
                ('column_value', models.TextField(max_length=1000)),
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
            name='Quarter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quarter_name', models.CharField(default=1, max_length=250, choices=[(b'JAN-MAR', b'JAN-MAR'), (b'APR-JUN', b'APR-JUN'), (b'JUL-SEPT', b'JUL-SEPT'), (b'OCT-DEC', b'OCT-DEC')])),
                ('quarter_year', models.IntegerField()),
                ('created_date', models.DateTimeField()),
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
        migrations.AlterUniqueTogether(
            name='quarter',
            unique_together=set([('quarter_name', 'quarter_year')]),
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
            field=models.ManyToManyField(to='umm_app.Quarter'),
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
            name='task',
            unique_together=set([('task_name', 'parent_category_id')]),
        ),
    ]
