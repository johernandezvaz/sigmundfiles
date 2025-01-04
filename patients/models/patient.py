from django.db import models
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