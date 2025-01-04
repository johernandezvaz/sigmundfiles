from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from patients.models import MedicalHistory
from patients.forms.medical import MedicalHistoryForm

class MedicalHistoryUpdateView(LoginRequiredMixin, UpdateView):
    model = MedicalHistory
    form_class = MedicalHistoryForm
    template_name = 'patients/medical_history_form.html'
    
    def get_queryset(self):
        return MedicalHistory.objects.filter(patient__psychologist=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('patient_detail', kwargs={'pk': self.object.patient.pk})