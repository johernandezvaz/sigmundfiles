from django import forms
from accounts.models import Psychologist

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Psychologist
        fields = ['email', 'first_name', 'last_name', 'institution']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True