from django import forms
from patients.models import Patient, Parent, Sibling, MedicalHistory, HouseholdMember

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = ['psychologist', 'created_at', 'updated_at']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'photo': forms.FileInput(attrs={'accept': 'image/*'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-input'
            
        # Personalizar etiquetas
        self.fields['photo'].label = 'Foto del paciente'
        self.fields['first_name'].label = 'Nombre(s)'
        self.fields['last_name'].label = 'Apellidos'
        self.fields['birth_date'].label = 'Fecha de nacimiento'
        self.fields['gender'].label = 'Género'
        self.fields['birthplace'].label = 'Lugar de nacimiento'
        self.fields['education_level'].label = 'Escolaridad'
        self.fields['marital_status'].label = 'Estado civil'
        self.fields['email'].label = 'Correo electrónico'
        self.fields['phone'].label = 'Teléfono'
        self.fields['address'].label = 'Dirección'
        self.fields['religion'].label = 'Religión'
        self.fields['voluntary_assistance'].label = '¿Acude voluntariamente?'