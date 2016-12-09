from django.contrib import admin
from django.db import models
from django import forms
from .models import Quarter, Category, Task, AdditionData, ColumnData, ComboUpdate, BudgetBand, Goal, Question, GoalTaskMap, ExtraTask, Process, ProgramType, ProgramTask, TaskData, AdditionDataReference, ProgramAdditionData
from umm_app.forms import AdditionDataAdminForm

class ComboInline(admin.TabularInline):
    model = ComboUpdate
    extra = 0


class QuarterAdmin(admin.ModelAdmin):
    inlines = [ComboInline, ]
    list_display = (u'quarter', 'quarter_year', 'created_date', 'modified_date')

    class Meta:
        model = Quarter


class BudgetBandAdmin(admin.ModelAdmin):
    list_display = ('parent_quarter_id', 'created_date', 'modified_date')
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
    list_display = ('parent_task_id','email_pitch_guidelines', 'implementation_guide', 'faq', 'elevator_pitch')
    formfield_overrides = {models.TextField: {'widget': forms.Textarea(attrs={'class':'ckeditor'})}, }

    form = AdditionDataAdminForm

    class Media:
        js = ('ckeditor/ckeditor.js',)

    class Meta:
        model = AdditionData


# -------------- Apollo -------------------
class ProcessAdmin(admin.ModelAdmin):
    list_display = ('name', 'url_name', 'image_ref', 'is_disabled')

    class Meta:
        model = Process


class ProgramTypeAdmin(admin.ModelAdmin):
    list_display = ('process', 'quarter', 'name', 'is_disabled')

    class Meta:
        model = ProgramType


class ProgramTaskAdmin(admin.ModelAdmin):
    list_display = ('program_type', 'name', 'is_disabled')

    class Meta:
        model = ProgramTask 


class TaskDataAdmin(admin.ModelAdmin):
    list_display = ('program_task', 'column_name', 'data', 'is_disabled')

    class Meta:
        model = TaskData


class AdditionDataReferenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_disabled')

    class Meta:
        model = AdditionDataReference


class ProgramAdditionDataAdmin(admin.ModelAdmin):
    list_display = ('program_task', 'additional_ref', 'quarter', 'data', 'is_disabled')

    class Meta:
        model = ProgramAdditionData            

# -------------- Apollo -------------------


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


# -------------- Apollo -------------------
admin.site.register(Process, ProcessAdmin)
admin.site.register(ProgramType, ProgramTypeAdmin)
admin.site.register(ProgramTask, ProgramTaskAdmin)
admin.site.register(TaskData, TaskDataAdmin)
admin.site.register(AdditionDataReference, AdditionDataReferenceAdmin)
admin.site.register(ProgramAdditionData, ProgramAdditionDataAdmin)