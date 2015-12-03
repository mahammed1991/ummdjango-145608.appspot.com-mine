from umm_app.models import AdditionData
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
