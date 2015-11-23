from django.contrib import admin
from django.db import models
from django import forms
from .models import Quarter, Category, Task, AdditionData, ColumnData, ComboUpdate, BudgetBand, Goal, Question, GoalTaskMap, ExtraTask


class ComboInline(admin.TabularInline):
    model = ComboUpdate
    extra = 0


class QuarterAdmin(admin.ModelAdmin):
    inlines = [ComboInline, ]
    list_display = ('quarter_name', 'quarter_year', 'created_date', 'modified_date')

    class Meta:
        model = Quarter


class BudgetBandAdmin(admin.ModelAdmin):
    list_display = ('band_details', 'created_date', 'modified_date')
    formfield_overrides = {models.TextField: {'widget': forms.Textarea(attrs={'class':'ckeditor'})}, }

    class Media:
        js = ('ckeditor/ckeditor.js',)

    class Meta:
        model = BudgetBand


class ComboUpdateAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_date', 'modified_date')
    formfield_overrides = {models.TextField: {'widget': forms.Textarea(attrs={'class':'ckeditor'})}, }

    class Media:
        js = ('ckeditor/ckeditor.js',)

    class Meta:
        model = ComboUpdate


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name', 'parent_quarter_id', 'created_date')

    class Meta:
        model = Category


class TaskAdmin(admin.ModelAdmin):
    # inlines = [ColumnDataInline, AdditionDataInline]
    list_display = ('task_name', 'parent_category_id', 'created_date')

    class Meta:
        model = Task


class GoalAdmin(admin.ModelAdmin):
    list_display = ('goal_name', 'created_date')

    class Meta:
        model = Goal


class ExtraTaskAdmin(admin.ModelAdmin):
    list_display = ('extra_task_name', 'parent_goal_id')

    class Meta:
        model = ExtraTask


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'parent_goal_id')

    class Meta:
        model = Question


class GoalTaskMapAdmin(admin.ModelAdmin):
    list_display = ('parent_goal_id', 'get_task', 'created_date')

    class Meta:
        model = GoalTaskMap


class ColumnDataAdmin(admin.ModelAdmin):
    list_display = ('column_name', 'parent_task_id', 'column_value')
    formfield_overrides = {models.TextField: {'widget': forms.Textarea(attrs={'class':'ckeditor'})}, }

    class Media:
        js = ('ckeditor/ckeditor.js',)

    class Meta:
        model = ColumnData


class AdditionDataAdmin(admin.ModelAdmin):
    list_display = ('email_pitch_guidelines', 'implementation_guide', 'faq', 'elevator_pitch')
    formfield_overrides = {models.TextField: {'widget': forms.Textarea(attrs={'class':'ckeditor'})}, }

    class Media:
        js = ('ckeditor/ckeditor.js',)

    class Meta:
        model = AdditionData


admin.site.register(Quarter, QuarterAdmin)
admin.site.register(BudgetBand, BudgetBandAdmin)
admin.site.register(ComboUpdate, ComboUpdateAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(ExtraTask, ExtraTaskAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(GoalTaskMap, GoalTaskMapAdmin)
admin.site.register(ColumnData, ColumnDataAdmin)
admin.site.register(AdditionData, AdditionDataAdmin)
