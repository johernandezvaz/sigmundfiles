from patients.views.patient import PatientListView, PatientCreateView, PatientDetailView, PatientUpdateView
from patients.views.medical_history import MedicalHistoryUpdateView

__all__ = [
    'PatientListView', 'PatientCreateView', 'PatientDetailView', 'PatientUpdateView',
    'MedicalHistoryUpdateView'
]