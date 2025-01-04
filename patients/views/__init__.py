from patients.views.patient import PatientListView, PatientCreateView, PatientDetailView, PatientUpdateView
from patients.views.medical_history import MedicalHistoryUpdateView
from patients.views.notes import PatientNotesListView, NoteCreateView, NoteUpdateView

__all__ = [
    'PatientListView', 'PatientCreateView', 'PatientDetailView', 'PatientUpdateView',
    'MedicalHistoryUpdateView',
    'PatientNotesListView', 'NoteCreateView', 'NoteUpdateView'
]