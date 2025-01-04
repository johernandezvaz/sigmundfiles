from django import forms
from patients.models import Parent, Sibling, HouseholdMember

class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        exclude = ['patient']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'pathological_history': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-input'

class SiblingForm(forms.ModelForm):
    class Meta:
        model = Sibling
        exclude = ['patient']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'pathological_history': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-input'

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