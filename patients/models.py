from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from simple_history.models import HistoricalRecords
from accounts.models import Psychologist

class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]
    
    MARITAL_STATUS_CHOICES = [
        ('S', 'Soltero/a'),
        ('C', 'Casado/a'),
        ('D', 'Divorciado/a'),
        ('V', 'Viudo/a'),
    ]

    psychologist = models.ForeignKey(Psychologist, on_delete=models.CASCADE, related_name='patients')
    photo = models.ImageField(upload_to='patient_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birthplace = models.CharField(max_length=200)
    education_level = models.CharField(max_length=100)
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_CHOICES)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    religion = models.CharField(max_length=100, blank=True)
    voluntary_assistance = models.BooleanField(default=True)
    
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

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

class HouseholdMember(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='household_members')
    name = models.CharField(max_length=200)
    relationship = models.CharField(max_length=100)
    medical_history = models.TextField(blank=True)
    history = HistoricalRecords()