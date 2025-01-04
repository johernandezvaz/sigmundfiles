import nltk
nltk.download('punkt_tab')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
from django.core.files.base import ContentFile

class TextAnalysisService:
    def __init__(self):
        # Descargar recursos necesarios de NLTK
        nltk.download('punkt')
        nltk.download('stopwords')
        self.stop_words = set(stopwords.words('spanish'))

    def process_text(self, text):
        """
        Procesa el texto y retorna las palabras relevantes con sus frecuencias
        """
        # Tokenización
        tokens = word_tokenize(text.lower())
        
        # Eliminar stopwords y palabras cortas
        words = [word for word in tokens 
                if word.isalnum() and 
                word not in self.stop_words and 
                len(word) > 2]
        
        # Calcular frecuencias
        freq_dist = nltk.FreqDist(words)
        
        return dict(freq_dist)

    def generate_wordcloud(self, frequencies):
        """
        Genera una nube de palabras a partir de las frecuencias
        """
        # Configurar WordCloud sin especificar una fuente
        wordcloud = WordCloud(
            width=800, 
            height=400,
            background_color='white',
            colormap='viridis',
            prefer_horizontal=0.7,
            relative_scaling=0.5,
            min_font_size=10,
            max_font_size=50,
            contour_width=3,
            contour_color='steelblue'
        ).generate_from_frequencies(frequencies)

        # Guardar la imagen
        image_stream = io.BytesIO()
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig(image_stream, format='png', bbox_inches='tight', pad_inches=0)
        plt.close()
        
        return ContentFile(image_stream.getvalue())