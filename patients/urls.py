from django.urls import path
from patients.views import patient, medical_history, debug, notes

urlpatterns = [
    path('', patient.PatientListView.as_view(), name='patient_list'),
    path('create/', patient.PatientCreateView.as_view(), name='patient_create'),
    path('<int:pk>/', patient.PatientDetailView.as_view(), name='patient_detail'),
    path('<int:pk>/edit/', patient.PatientUpdateView.as_view(), name='patient_edit'),
    path('<int:pk>/medical-history/', medical_history.MedicalHistoryUpdateView.as_view(), name='medical_history'),
    # Rutas para notas
    path('<int:pk>/notes/', notes.PatientNotesListView.as_view(), name='patient_notes'),
    path('<int:pk>/notes/create/', notes.NoteCreateView.as_view(), name='note_create'),
    path('notes/<int:pk>/edit/', notes.NoteUpdateView.as_view(), name='note_edit'),
    path('notes/<int:pk>/delete/', notes.NoteDeleteView.as_view(), name='note_delete'),
    # Vista de depuración temporal
    path('<int:pk>/debug/', debug.debug_patient_data, name='debug_patient_data'),
]