from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import model_to_dict
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.db import transaction
from patients.models import Patient, Parent, Sibling, HouseholdMember, MedicalHistory
from patients.forms.patient import PatientForm
from patients.constants import MEDICAL_HISTORY_QUESTIONS
from patients.services.patient_form_handler import PatientFormHandler

class PatientListView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'patients/patient_list.html'
    context_object_name = 'patients'

    def get_queryset(self):
        return Patient.objects.filter(psychologist=self.request.user)

class PatientCreateView(LoginRequiredMixin, CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patients/patient_form.html'
    success_url = reverse_lazy('patient_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['medical_questions'] = MEDICAL_HISTORY_QUESTIONS
        return context

    @transaction.atomic
    def form_valid(self, form):
        # Asignar el psicólogo actual
        form.instance.psychologist = self.request.user
        response = super().form_valid(form)
        
        # Crear historial médico
        medical_data = {}
        for question in MEDICAL_HISTORY_QUESTIONS:
            field_id = question['id']
            value = self.request.POST.get(f'medical_{field_id}')
            if value:
                medical_data[field_id] = value
        
        if medical_data:
            MedicalHistory.objects.create(patient=self.object, **medical_data)

        # Procesar padres
        parents_data = self.request.POST.getlist('parents[][name]')
        for i, name in enumerate(parents_data):
            if name:
                Parent.objects.create(
                    patient=self.object,
                    name=name,
                    birth_date=self.request.POST.getlist('parents[][birth_date]')[i],
                    education_level=self.request.POST.getlist('parents[][education_level]')[i],
                    occupation=self.request.POST.getlist('parents[][occupation]')[i],
                    pathological_history=self.request.POST.getlist('parents[][pathological_history]')[i]
                )

        # Procesar hermanos
        siblings_data = self.request.POST.getlist('siblings[][name]')
        for i, name in enumerate(siblings_data):
            if name:
                Sibling.objects.create(
                    patient=self.object,
                    name=name,
                    birth_date=self.request.POST.getlist('siblings[][birth_date]')[i],
                    education_level=self.request.POST.getlist('siblings[][education_level]')[i],
                    has_addictions=self.request.POST.getlist('siblings[][has_addictions]')[i] == 'on',
                    pathological_history=self.request.POST.getlist('siblings[][pathological_history]')[i]
                )

        # Procesar habitantes del hogar
        household_data = self.request.POST.getlist('household[][name]')
        for i, name in enumerate(household_data):
            if name:
                HouseholdMember.objects.create(
                    patient=self.object,
                    name=name,
                    relationship=self.request.POST.getlist('household[][relationship]')[i],
                    medical_history=self.request.POST.getlist('household[][medical_history]')[i]
                )

        return response


class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = 'patients/patient_detail.html'
    context_object_name = 'patient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['medical_questions'] = MEDICAL_HISTORY_QUESTIONS
        return context

    def get_queryset(self):
        return Patient.objects.filter(psychologist=self.request.user)

class PatientUpdateView(LoginRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patients/patient_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            # Convertir el historial médico a diccionario si existe
            medical_history = None
            if hasattr(self.object, 'medical_history'):
                medical_history = model_to_dict(
                    self.object.medical_history,
                    exclude=['id', 'patient']
                )

            # Preparar datos existentes
            context['existing_data'] = {
                'medical_history': medical_history,
                'parents': [
                    model_to_dict(parent, exclude=['id', 'patient']) 
                    for parent in self.object.parents.all()
                ],
                'siblings': [
                    model_to_dict(sibling, exclude=['id', 'patient']) 
                    for sibling in self.object.siblings.all()
                ],
                'household_members': [
                    model_to_dict(member, exclude=['id', 'patient']) 
                    for member in self.object.household_members.all()
                ]
            }
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        handler = PatientFormHandler(self.request, self.object)
        handler.handle_medical_history()
        handler.handle_family_members()
        return response

    
    @transaction.atomic
    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Actualizar historial médico
        medical_data = {}
        for question in MEDICAL_HISTORY_QUESTIONS:
            field_id = question['id']
            value = self.request.POST.get(f'medical_{field_id}')
            if value:
                medical_data[field_id] = value
        
        if medical_data:
            MedicalHistory.objects.update_or_create(
                patient=self.object,
                defaults=medical_data
            )

        # Limpiar datos familiares existentes
        self.object.parents.all().delete()
        self.object.siblings.all().delete()
        self.object.household_members.all().delete()

        # Procesar padres
        parents_data = self.request.POST.getlist('parents[][name]')
        for i, name in enumerate(parents_data):
            if name:
                Parent.objects.create(
                    patient=self.object,
                    name=name,
                    birth_date=self.request.POST.getlist('parents[][birth_date]')[i],
                    education_level=self.request.POST.getlist('parents[][education_level]')[i],
                    occupation=self.request.POST.getlist('parents[][occupation]')[i],
                    pathological_history=self.request.POST.getlist('parents[][pathological_history]')[i]
                )

        # Procesar hermanos
        siblings_data = self.request.POST.getlist('siblings[][name]')
        for i, name in enumerate(siblings_data):
            if name:
                Sibling.objects.create(
                    patient=self.object,
                    name=name,
                    birth_date=self.request.POST.getlist('siblings[][birth_date]')[i],
                    education_level=self.request.POST.getlist('siblings[][education_level]')[i],
                    has_addictions=self.request.POST.getlist('siblings[][has_addictions]')[i] == 'on',
                    pathological_history=self.request.POST.getlist('siblings[][pathological_history]')[i]
                )

        # Procesar habitantes del hogar
        household_data = self.request.POST.getlist('household[][name]')
        for i, name in enumerate(household_data):
            if name:
                HouseholdMember.objects.create(
                    patient=self.object,
                    name=name,
                    relationship=self.request.POST.getlist('household[][relationship]')[i],
                    medical_history=self.request.POST.getlist('household[][medical_history]')[i]
                )

        return response
    
    def get_success_url(self):
        return reverse_lazy('patient_detail', kwargs={'pk': self.object.pk})
