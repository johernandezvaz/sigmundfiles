from django import forms
from patients.models import HouseholdMember

class HouseholdMemberForm(forms.ModelForm):
    class Meta:
        model = HouseholdMember
        exclude = ['patient']
        widgets = {
            'medical_history': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-input'