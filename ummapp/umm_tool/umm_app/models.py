from django.db import models
from django.contrib.auth.models import User

class Quarter(models.Model):
    QUARTER_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
    )
    quarter = models.IntegerField(choices=QUARTER_CHOICES, default=1)
    quarter_year = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('quarter', 'quarter_year',)

    def __unicode__(self):
            return u"%s-%d" % (self.quarter, self.quarter_year)


class BudgetBand(models.Model):
    parent_quarter_id = models.ForeignKey(Quarter)
    band_details = models.TextField()
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s" % (self.band_details)


class ComboUpdate(models.Model):
    parent_quarter_id = models.ForeignKey(Quarter)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s %s" % (self.title, self.description)


class Category(models.Model):
    parent_quarter_id = models.ForeignKey(Quarter)
    category_name = models.CharField(max_length=250, unique=True)
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField(auto_now=True)
    is_disable = models.BooleanField(default=False)

    class Meta:
        unique_together = ('category_name', 'parent_quarter_id',)

    def __unicode__(self):
        return "%s-%s" % (self.category_name, self.parent_quarter_id)


class Task(models.Model):
    parent_category_id = models.ForeignKey(Category)
    task_name = models.CharField(max_length=250)
    created_date = models.DateField()
    modified_date = models.DateTimeField(auto_now=True)
    is_disable = models.BooleanField(default=False)

    class Meta:
        unique_together = ('task_name', 'parent_category_id',)

    def __unicode__(self):
        return "%s|%s" % (self.task_name, self.parent_category_id)


class Goal(models.Model):
    goal_name = models.CharField(max_length=250)
    created_date = models.DateField()
    modified_date = models.DateTimeField(auto_now=True)
    is_disable = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s" % (self.goal_name)


class Question(models.Model):
    parent_goal_id = models.ForeignKey(Goal)
    question = models.CharField(max_length=500)

    def __unicode__(self):
        return "%s" % (self.question)


class ExtraTask(models.Model):
    parent_goal_id = models.ForeignKey(Goal)
    extra_task_name = models.CharField(max_length=500)

    def __unicode__(self):
        return "%s" % (self.extra_task_name)


class GoalTaskMap(models.Model):
    parent_task_id = models.ManyToManyField(Task)
    parent_goal_id = models.ForeignKey(Goal)
    created_date = models.DateField()
    modified_date = models.DateTimeField(auto_now=True)
    is_disable = models.BooleanField(default=False)

    def get_task(self):
        return "\n".join(['%s-%s' % (q.task_name, q.parent_category_id) for q in self.parent_task_id.all()])

    def __unicode__(self):
        return "%s %s" % (self.parent_task_id, self.parent_goal_id)


class ColumnData(models.Model):
    parent_task_id = models.ForeignKey(Task)
    column_name = models.CharField(max_length=250)
    column_value = models.TextField()
    is_disable = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s %s %s" % (self.column_name, self.column_name, self.column_value)


class AdditionData(models.Model):
    parent_task_id = models.ForeignKey(Task)
    email_pitch_guidelines = models.TextField()
    implementation_guide = models.TextField()
    faq = models.TextField()
    elevator_pitch = models.TextField()
    is_disable = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s %s %s %s" % (self.email_pitch_guidelines, self.implementation_guide,self.faq,self.elevator_pitch)

# -------------- Appolo -------------------

class Process(models.Model):
    # Convert url_name to lowercase and replace space by -
    name = models.CharField(max_length=250, unique=True)
    url_name = models.CharField(max_length=250, unique=True)
    image_ref = models.ImageField(upload_to='processes/', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_disabled = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='process_created_by', null=False)
    modified_by = models.ForeignKey(User, related_name='process_modified_by', null=False)

    def __unicode__(self):
        return "%s" % (self.name)


class SubProcess(models.Model):
    # Convert url_name to lowercase and replace space by 
    process = models.ForeignKey(Process)
    quarter = models.ForeignKey(Quarter)
    name = models.CharField(max_length=250)
    cloned_count = models.IntegerField(default=0)
    url_name = models.CharField(max_length=250)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_disabled = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='subprocess_created_by', null=False)
    modified_by = models.ForeignKey(User, related_name='subprocess_modified_by', null=False)

    class Meta:
        unique_together = ('process', 'name', 'quarter',)

    def __unicode__(self):
        return "%s" % (self.name)


class ProgramType(models.Model):
    subprocess = models.ForeignKey(SubProcess)
    name = models.CharField(max_length=250)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_disabled = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='programtype_created_by', null=False)
    modified_by = models.ForeignKey(User, related_name='programtype_modified_by', null=False)

    class Meta:
        unique_together = ('subprocess', 'name')

    def __unicode__(self):
        return "%s" % (self.name)


class ProgramTask(models.Model):
    program_type = models.ForeignKey(ProgramType)
    name = models.CharField(max_length=250)
    created_date = models.DateField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_disabled = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='programtask_created_by', null=False)
    modified_by = models.ForeignKey(User, related_name='programtask_modified_by', null=False)

    class Meta:
        unique_together = ('name', 'program_type',)

    def __unicode__(self):
        return "%s|%s" % (self.name, self.program_type)


class TaskData(models.Model):
    program_task = models.ForeignKey(ProgramTask)
    column_name = models.CharField(max_length=250)
    column_number = models.IntegerField(default=0,null=True, blank=True)
    data = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_disabled = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='taskdata_created_by', null=False)
    modified_by = models.ForeignKey(User, related_name='taskdata_modified_by', null=False)

    class Meta:
        unique_together = ('column_name', 'program_task',)

    def __unicode__(self):
        return "%s %s %s" % (self.program_task, self.column_name, self.data)


class SubProcessLevelUpdates(models.Model):
    subprocess = models.ForeignKey(SubProcess)
    name = models.CharField(max_length=250)
    data = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='subprocessupdates_created_by', null=False)
    modified_by = models.ForeignKey(User, related_name='subprocessupdates_modified_by', null=False)

    class Meta:
        unique_together = ('subprocess', 'name')
        
    def __unicode__(self):
        return "%s" % (self.name)


class ProgramAdditionData(models.Model):
    program_task = models.ForeignKey(ProgramTask)
    name = models.CharField(max_length=250)
    data = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_disabled = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='adddata_created_by', null=False)
    modified_by = models.ForeignKey(User, related_name='adddata_modified_by', null=False)
   
    class Meta:
        unique_together = ('program_task', 'name')

    def __unicode__(self):
        return "%s %s" % (self.program_task, self.name)


class Faq(models.Model):
    program_type = models.ForeignKey(ProgramType, null=True, blank=True)
    program_task = models.ForeignKey(ProgramTask, null=True, blank=True)
    question = models.TextField()
    answer = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='faq_created_by', null=False)
    modified_by = models.ForeignKey(User, related_name='faq_modified_by', null=False)

    def __unicode__(self):
         return "%s %s %s %s" % (self.program_type, self.program_task, self.question, self.answer)


class QualityFramework(models.Model):
    name = models.CharField(max_length=250, unique=True)
    data = models.TextField()    
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='qualityframework_created_by', null=False)
    modified_by = models.ForeignKey(User, related_name='qualityframework_modified_by', null=False)    

    def __unicode__(self):
        return "%s %s" % (self.name, self.data)



