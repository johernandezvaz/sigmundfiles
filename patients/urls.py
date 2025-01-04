from django.urls import path
from patients.views import patient, medical_history, debug

urlpatterns = [
    path('', patient.PatientListView.as_view(), name='patient_list'),
    path('create/', patient.PatientCreateView.as_view(), name='patient_create'),
    path('<int:pk>/', patient.PatientDetailView.as_view(), name='patient_detail'),
    path('<int:pk>/edit/', patient.PatientUpdateView.as_view(), name='patient_edit'),
    path('<int:pk>/medical-history/', medical_history.MedicalHistoryUpdateView.as_view(), name='medical_history'),
    # Vista de depuración temporal
    path('<int:patient_id>/debug/', debug.debug_patient_data, name='debug_patient_data'),
]