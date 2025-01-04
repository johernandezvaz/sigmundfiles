from django.db import transaction
from patients.models import Parent, Sibling, HouseholdMember, MedicalHistory

class PatientFormHandler:
    def __init__(self, request, patient):
        self.request = request
        self.patient = patient
        self.post_data = request.POST

    @transaction.atomic
    def handle_medical_history(self):
        medical_data = {}
        for key, value in self.post_data.items():
            if key.startswith('medical_') and value:
                field_name = key.replace('medical_', '')
                medical_data[field_name] = value
        
        if medical_data:
            MedicalHistory.objects.update_or_create(
                patient=self.patient,
                defaults=medical_data
            )

    @transaction.atomic
    def handle_family_members(self):
        # Limpiar datos existentes
        self.patient.parents.all().delete()
        self.patient.siblings.all().delete()
        self.patient.household_members.all().delete()

        # Procesar padres
        parent_names = self.post_data.getlist('parent_name[]')
        for i in range(len(parent_names)):
            if parent_names[i]:
                Parent.objects.create(
                    patient=self.patient,
                    name=parent_names[i],
                    birth_date=self.post_data.getlist('parent_birth_date[]')[i],
                    education_level=self.post_data.getlist('parent_education_level[]')[i],
                    occupation=self.post_data.getlist('parent_occupation[]')[i],
                    pathological_history=self.post_data.getlist('parent_pathological_history[]')[i]
                )

        # Procesar hermanos
        sibling_names = self.post_data.getlist('sibling_name[]')
        for i in range(len(sibling_names)):
            if sibling_names[i]:
                Sibling.objects.create(
                    patient=self.patient,
                    name=sibling_names[i],
                    birth_date=self.post_data.getlist('sibling_birth_date[]')[i],
                    education_level=self.post_data.getlist('sibling_education_level[]')[i],
                    has_addictions=bool(self.post_data.getlist('sibling_has_addictions[]')[i]),
                    pathological_history=self.post_data.getlist('sibling_pathological_history[]')[i]
                )

        # Procesar habitantes del hogar
        household_names = self.post_data.getlist('household_name[]')
        for i in range(len(household_names)):
            if household_names[i]:
                HouseholdMember.objects.create(
                    patient=self.patient,
                    name=household_names[i],
                    relationship=self.post_data.getlist('household_relationship[]')[i],
                    medical_history=self.post_data.getlist('household_medical_history[]')[i]
                )