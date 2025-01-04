from django.db import models
from simple_history.models import HistoricalRecords
from patients.models.patient import Patient

class MedicalHistory(models.Model):
    CONDITION_CHOICES = [
        ('N', 'Nunca'),
        ('P', 'Pasado'),
        ('A', 'Presente'),
    ]

    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='medical_history')
    asthma_allergies = models.CharField(max_length=1, choices=CONDITION_CHOICES)
    frequent_colds = models.CharField(max_length=1, choices=CONDITION_CHOICES)
    epilepsy_seizures = models.CharField(max_length=1, choices=CONDITION_CHOICES)
    febrile_seizures = models.CharField(max_length=1, choices=CONDITION_CHOICES)
    manias = models.CharField(max_length=1, choices=CONDITION_CHOICES)
    head_injuries = models.CharField(max_length=1, choices=CONDITION_CHOICES)
    surgeries_hospitalizations = models.CharField(max_length=1, choices=CONDITION_CHOICES)
    vision_problems = models.CharField(max_length=1, choices=CONDITION_CHOICES)
    appetite_problems = models.CharField(max_length=1, choices=CONDITION_CHOICES)
    history = HistoricalRecords()