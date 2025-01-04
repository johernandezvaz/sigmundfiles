from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import Psychologist
from django.core.exceptions import ValidationError

class PsychologistRegistrationForm(UserCreationForm):
    class Meta:
        model = Psychologist
        fields = ['email', 'professional_license', 'first_name', 'last_name', 
                 'institution', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['professional_license'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        
        # Agregar clases CSS a los campos
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-input'
            
        # Personalizar etiquetas
        self.fields['email'].label = 'Correo electrónico'
        self.fields['professional_license'].label = 'Cédula Profesional'
        self.fields['first_name'].label = 'Nombre'
        self.fields['last_name'].label = 'Apellido'
        self.fields['institution'].label = 'Institución'
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirmar contraseña'
        
        # Personalizar placeholders
        self.fields['email'].widget.attrs['placeholder'] = 'nombre@ejemplo.com'
        self.fields['professional_license'].widget.attrs['placeholder'] = 'Número de cédula profesional'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Tu nombre'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Tu apellido'
        self.fields['institution'].widget.attrs['placeholder'] = 'Lugar donde trabajas'
        self.fields['password1'].widget.attrs['placeholder'] = '••••••••'
        self.fields['password2'].widget.attrs['placeholder'] = '••••••••'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Psychologist.objects.filter(email=email).exists():
            raise ValidationError(
                "Ya existe una cuenta con este correo electrónico. Por favor, utiliza otro correo o inicia sesión.",
                code='email_exists'
            )
        return email

    def clean_professional_license(self):
        license = self.cleaned_data.get('professional_license')
        if Psychologist.objects.filter(professional_license=license).exists():
            raise ValidationError(
                "Esta cédula profesional ya está registrada. Si crees que esto es un error, por favor contáctanos.",
                code='license_exists'
            )
        return license

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user