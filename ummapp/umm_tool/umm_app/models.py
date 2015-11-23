from django.db import models


class Quarter(models.Model):
    QUARTER_CHOICES = (
        ('JAN-MAR', 'JAN-MAR'),
        ('APR-JUN', 'APR-JUN'),
        ('JUL-SEPT', 'JUL-SEPT'),
        ('OCT-DEC', 'OCT-DEC'),
    )
    quarter_name = models.CharField(max_length=250, choices=QUARTER_CHOICES, default=1)
    quarter_year = models.IntegerField()
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('quarter_name', 'quarter_year',)

    def __unicode__(self):
            return "%s-%s" % (self.quarter_name, self.quarter_year)


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
    column_value = models.TextField(max_length=1000)
    is_disable = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s %s %s" % (self.column_name, self.column_name, self.column_value)


class AdditionData(models.Model):
    parent_task_id = models.ForeignKey(Task)
    email_pitch_guidelines = models.CharField(max_length=250)
    implementation_guide = models.CharField(max_length=250)
    faq = models.CharField(max_length=250)
    elevator_pitch = models.TextField(max_length=1000)
    is_disable = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s %s %s %s" % (self.email_pitch_guidelines, self.implementation_guide,self.faq,self.elevator_pitch)
