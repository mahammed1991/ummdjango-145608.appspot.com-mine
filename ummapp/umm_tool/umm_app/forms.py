from umm_app.models import AdditionData, Process, ProgramType, ProgramTask, TaskData
from django import forms

class AdditionDataAdminForm(forms.ModelForm):
    class Meta:
        model = AdditionData
        fields = ('parent_task_id','email_pitch_guidelines', 'implementation_guide', 'faq', 'elevator_pitch')

    def clean(self):
        cleaned_data = self.cleaned_data
        pk = self.instance.pk
        if cleaned_data.get('parent_task_id'):
        	parent_task_id = cleaned_data.get('parent_task_id').id
        	addition_data_record = AdditionData.objects.filter(parent_task_id=parent_task_id)
        	if len(addition_data_record) == 1 and (addition_data_record[0].id != pk):
        		raise forms.ValidationError(u"Addition data record with selected task already exists")
        return cleaned_data


class ProcessForm(forms.ModelForm):
    class Meta:
        model = Process
        fields = ('name','image_ref', 'is_disabled')
    """
    def clean(self):
        cleaned_data = self.cleaned_data
        pk = self.instance.pk
        if not cleaned_data.get('name'):
            raise forms.ValidationError(u"Name is required")

        if not cleaned_data.get('image_ref'):
            raise forms.ValidationError(u"Image ref is required")

        import pdb
        pdb.set_trace() 
        if cleaned_data.get('name'):
            process_exists = Process.objects.filter(name=cleaned_data.get('name'))
            if process_exists:
                print "in"
                raise forms.ValidationError(u"Process with this Name already exists")
        return cleaned_data
        """

class ProgramTypeForm(forms.ModelForm):
    class Meta:
        model = ProgramType
        fields = ('process','quarter','name','is_disabled')


class ProgramTaskForm(forms.ModelForm):
    class Meta:
        model = ProgramTask
        fields = ('program_type','name', 'is_disabled')


class TaskDataForm(forms.ModelForm):
    class Meta:
        model = TaskData
        fields = ('program_task','column_name','data','is_disabled')