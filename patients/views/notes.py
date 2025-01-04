from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from patients.models import Patient, HandwrittenNote
from patients.forms.notes import HandwrittenNoteForm, NoteTextForm
from patients.services.ocr.error_handler import OCRErrorHandler
from patients.services.ocr.trocr_service import TrOCRService
from patients.services.word_cloud_service import WordCloudService

class PatientNotesListView(LoginRequiredMixin, ListView):
    model = HandwrittenNote
    template_name = 'patients/notes/list.html'
    context_object_name = 'notes'

    def get_queryset(self):
        self.patient = get_object_or_404(
            Patient, 
            id=self.kwargs['pk'],
            psychologist=self.request.user
        )
        return self.patient.handwritten_notes.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = self.patient
        # Obtener nube de palabras individual del paciente
        try:
            context['word_cloud'] = self.patient.word_clouds.get(cloud_type='individual')
        except:
            pass
        return context

class NoteCreateView(LoginRequiredMixin, CreateView):
    model = HandwrittenNote
    form_class = HandwrittenNoteForm
    template_name = 'patients/notes/create.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = get_object_or_404(Patient, pk=self.kwargs['pk'])
        return context
    
    def form_valid(self, form):
        note = form.save(commit=False)
        note.patient = get_object_or_404(Patient, pk=self.kwargs['pk'])
        
        # Process image with TrOCR
        ocr_service = TrOCRService()
        recognized_text = ocr_service.process_image(note.image.path)
        
        if recognized_text:
            note.digitized_text = recognized_text
            note.corrected_text = recognized_text  # Initial value same as digitized
            note.save()
            
            # Update word clouds
            word_cloud_service = WordCloudService()
            word_cloud_service.update_word_clouds(note.patient, recognized_text)
            
            messages.success(self.request, 'Nota creada exitosamente')
            return HttpResponseRedirect(self.get_success_url())
        else:
            OCRErrorHandler.handle_ocr_error(self.request, "no_text")
            return self.form_invalid(form)
    
    def get_success_url(self):
        return reverse_lazy('patient_notes', kwargs={'pk': self.kwargs['pk']})

class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = HandwrittenNote
    form_class = NoteTextForm
    template_name = 'patients/notes/edit.html'

    def get_queryset(self):
        return HandwrittenNote.objects.filter(patient__psychologist=self.request.user)

    def get_success_url(self):
        return reverse_lazy('patient_notes', kwargs={'pk': self.object.patient.id})

    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Actualizar nube de palabras con el texto corregido
        word_cloud_service = WordCloudService()
        word_cloud_service.update_word_clouds(self.object.patient, form.instance.corrected_text)
        
        return response

class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = HandwrittenNote
    template_name = 'patients/notes/delete.html'
    
    def get_queryset(self):
        return HandwrittenNote.objects.filter(patient__psychologist=self.request.user)
    
    def get_success_url(self):
        messages.success(self.request, 'La nota ha sido eliminada exitosamente.')
        return reverse_lazy('patient_notes', kwargs={'pk': self.object.patient.id})
    
    def delete(self, request, *args, **kwargs):
        """Sobrescribir delete para asegurar que la imagen y nubes se eliminen correctamente"""
        self.object = self.get_object()
        success_url = self.get_success_url()
        patient = self.object.patient
        
        # Eliminar la imagen del sistema de archivos
        if self.object.image:
            self.object.image.delete(save=False)
            
        # Eliminar el objeto
        self.object.delete()
        
        # Recalcular nubes de palabras
        word_cloud_service = WordCloudService()
        word_cloud_service.recalculate_clouds_after_deletion(patient)
        
        return HttpResponseRedirect(success_url)