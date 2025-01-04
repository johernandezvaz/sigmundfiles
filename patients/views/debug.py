from django.http import JsonResponse
from patients.models import Patient, MedicalHistory

def debug_patient_data(request, patient_id):
    """Vista temporal para depuración de datos del paciente"""
    try:
        patient = Patient.objects.get(id=patient_id)
        
        # Datos básicos del paciente
        patient_data = {
            'id': patient.id,
            'name': f"{patient.first_name} {patient.last_name}",
            'email': patient.email,
            'phone': patient.phone,
            'birth_date': str(patient.birth_date),
            'gender': patient.get_gender_display(),
            'marital_status': patient.get_marital_status_display(),
        }
        
        # Historial médico
        if hasattr(patient, 'medical_history'):
            medical_data = {
                'asthma_allergies': patient.medical_history.get_asthma_allergies_display(),
                'frequent_colds': patient.medical_history.get_frequent_colds_display(),
                'epilepsy_seizures': patient.medical_history.get_epilepsy_seizures_display(),
                'febrile_seizures': patient.medical_history.get_febrile_seizures_display(),
                'manias': patient.medical_history.get_manias_display(),
                'head_injuries': patient.medical_history.get_head_injuries_display(),
                'surgeries_hospitalizations': patient.medical_history.get_surgeries_hospitalizations_display(),
                'vision_problems': patient.medical_history.get_vision_problems_display(),
                'appetite_problems': patient.medical_history.get_appetite_problems_display(),
            }
        else:
            medical_data = None
        
        # Información familiar
        family_data = {
            'parents': [{
                'name': p.name,
                'birth_date': str(p.birth_date),
                'education_level': p.education_level,
                'occupation': p.occupation,
                'pathological_history': p.pathological_history
            } for p in patient.parents.all()],
            
            'siblings': [{
                'name': s.name,
                'birth_date': str(s.birth_date),
                'education_level': s.education_level,
                'has_addictions': s.has_addictions,
                'pathological_history': s.pathological_history
            } for s in patient.siblings.all()],
            
            'household_members': [{
                'name': h.name,
                'relationship': h.relationship,
                'medical_history': h.medical_history
            } for h in patient.household_members.all()]
        }
        
        return JsonResponse({
            'patient': patient_data,
            'medical_history': medical_data,
            'family': family_data
        }, json_dumps_params={'indent': 2})
        
    except Patient.DoesNotExist:
        return JsonResponse({'error': 'Paciente no encontrado'}, status=404)