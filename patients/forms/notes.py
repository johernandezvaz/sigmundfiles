from django import forms
from patients.models import HandwrittenNote

class HandwrittenNoteForm(forms.ModelForm):
    class Meta:
        model = HandwrittenNote
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-input',
                'accept': 'image/*'
            })
        }

class NoteTextForm(forms.ModelForm):
    class Meta:
        model = HandwrittenNote
        fields = ['corrected_text']
        widgets = {
            'corrected_text': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 10,
                'placeholder': 'Texto digitalizado...'
            })
        }