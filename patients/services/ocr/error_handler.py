from django.contrib import messages

class OCRErrorHandler:
    @staticmethod
    def handle_ocr_error(request, error_type="general"):
        """Handle different types of OCR errors and show appropriate messages"""
        error_messages = {
            "no_text": "No se pudo detectar texto en la imagen. Por favor, asegúrate de que la imagen sea clara y legible.",
            "processing": "Hubo un error al procesar la imagen. Por favor, intenta nuevamente.",
            "general": "Ocurrió un error inesperado. Por favor, intenta nuevamente."
        }
        
        message = error_messages.get(error_type, error_messages["general"])
        messages.error(request, message)