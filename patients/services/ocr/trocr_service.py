from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import torch

class TrOCRService:
    def __init__(self):
        self.processor = TrOCRProcessor.from_pretrained('microsoft/trocr-large-handwritten')
        self.model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-large-handwritten')
        
        # Move to GPU if available
        if torch.cuda.is_available():
            self.model.to('cuda')

    def process_image(self, image_path):
        try:
            # Load and preprocess image
            image = Image.open(image_path).convert('RGB')
            pixel_values = self.processor(image, return_tensors="pt").pixel_values
            
            if torch.cuda.is_available():
                pixel_values = pixel_values.to('cuda')

            # Generate text
            generated_ids = self.model.generate(pixel_values)
            generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            
            return self.postprocess_text(generated_text)
            
        except Exception as e:
            print(f"Error in OCR: {str(e)}")
            return None

    def postprocess_text(self, text):
        """Clean and improve the recognized text"""
        if not text:
            return None
            
        # Remove unwanted characters
        text = ''.join(c for c in text if c.isprintable())
        
        # Fix common spacing issues
        text = ' '.join(text.split())
        
        # Fix punctuation
        text = text.replace(' ,', ',')
        text = text.replace(' .', '.')
        text = text.replace(' :', ':')
        
        # Capitalize sentences
        sentences = text.split('. ')
        sentences = [s.capitalize() for s in sentences]
        text = '. '.join(sentences)
        
        return text.strip()