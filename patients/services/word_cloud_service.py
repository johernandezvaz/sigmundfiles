from patients.models import WordCloud, HandwrittenNote
from patients.services.text_analysis_service import TextAnalysisService

class WordCloudService:
    def __init__(self):
        self.text_analysis = TextAnalysisService()

    def update_word_clouds(self, patient, text):
        """
        Actualiza las nubes de palabras para un paciente específico y la nube global
        """
        # Procesar el texto
        frequencies = self.text_analysis.process_text(text)
        
        # Actualizar nube individual del paciente
        self._update_cloud(patient, frequencies, 'individual')
        
        # Actualizar nube global
        self._update_global_cloud(frequencies)

    def _update_cloud(self, patient, frequencies, cloud_type):
        """
        Actualiza o crea una nube de palabras específica
        """
        # Si no hay frecuencias y es una nube individual, eliminar la nube existente
        if not frequencies and cloud_type == 'individual':
            WordCloud.objects.filter(patient=patient, cloud_type=cloud_type).delete()
            return

        # Generar imagen de nube de palabras
        image_content = self.text_analysis.generate_wordcloud(frequencies)
        
        # Actualizar o crear nube de palabras
        cloud, created = WordCloud.objects.get_or_create(
            patient=patient if cloud_type == 'individual' else None,
            cloud_type=cloud_type,
            defaults={'data': frequencies}
        )
        
        if not created:
            # Combinar frecuencias existentes con nuevas
            existing_data = cloud.data
            for word, freq in frequencies.items():
                existing_data[word] = existing_data.get(word, 0) + freq
            cloud.data = existing_data
        
        # Guardar nueva imagen
        cloud.image.save(
            f'wordcloud_{cloud_type}_{patient.id if patient else "global"}.png',
            image_content,
            save=True
        )

    def _update_global_cloud(self, frequencies):
        """
        Actualiza la nube de palabras global o la elimina si no hay más notas
        """
        # Verificar si hay notas en el sistema
        if HandwrittenNote.objects.exists():
            self._update_cloud(None, frequencies, 'global')
        else:
            # Si no hay notas, eliminar la nube global
            WordCloud.objects.filter(cloud_type='global').delete()

    def recalculate_clouds_after_deletion(self, patient):
        """
        Recalcula las nubes de palabras después de eliminar una nota
        """
        # Recalcular nube individual si el paciente aún tiene notas
        patient_notes = HandwrittenNote.objects.filter(patient=patient)
        if patient_notes.exists():
            # Combinar texto de todas las notas restantes
            all_text = ' '.join(note.corrected_text for note in patient_notes)
            frequencies = self.text_analysis.process_text(all_text)
            self._update_cloud(patient, frequencies, 'individual')
        else:
            # Si no hay más notas, eliminar la nube individual
            WordCloud.objects.filter(patient=patient, cloud_type='individual').delete()

        # Recalcular nube global
        all_notes = HandwrittenNote.objects.all()
        if all_notes.exists():
            # Combinar texto de todas las notas del sistema
            all_text = ' '.join(note.corrected_text for note in all_notes)
            frequencies = self.text_analysis.process_text(all_text)
            self._update_cloud(None, frequencies, 'global')
        else:
            # Si no hay más notas en el sistema, eliminar la nube global
            WordCloud.objects.filter(cloud_type='global').delete()