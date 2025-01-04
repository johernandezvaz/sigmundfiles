from django import forms
from patients.models import MedicalHistory

class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        exclude = ['patient']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-input'