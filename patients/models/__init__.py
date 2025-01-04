from django.db import models
from simple_history.models import HistoricalRecords
from accounts.models import Psychologist

# Importar los modelos base
from patients.models.patient import Patient
from patients.models.family import Parent, Sibling, HouseholdMember
from patients.models.medical import MedicalHistory
from patients.models.notes import HandwrittenNote, WordCloud

__all__ = [
    'Patient',
    'Parent',
    'Sibling',
    'HouseholdMember',
    'MedicalHistory',
    'HandwrittenNote',
    'WordCloud'
]