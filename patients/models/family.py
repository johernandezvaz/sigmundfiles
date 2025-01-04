from django.db import models
from simple_history.models import HistoricalRecords
from patients.models.patient import Patient

class Parent(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='parents')
    name = models.CharField(max_length=200)
    birth_date = models.DateField()
    education_level = models.CharField(max_length=100)
    occupation = models.CharField(max_length=200)
    pathological_history = models.TextField(blank=True)
    history = HistoricalRecords()

class Sibling(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='siblings')
    name = models.CharField(max_length=200)
    birth_date = models.DateField()
    education_level = models.CharField(max_length=100)
    pathological_history = models.TextField(blank=True)
    has_addictions = models.BooleanField(default=False)
    history = HistoricalRecords()

class HouseholdMember(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='household_members')
    name = models.CharField(max_length=200)
    relationship = models.CharField(max_length=100)
    medical_history = models.TextField(blank=True)
    history = HistoricalRecords()