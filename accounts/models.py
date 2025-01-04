from django.contrib.auth.models import AbstractUser
from django.db import models
from simple_history.models import HistoricalRecords

class Psychologist(AbstractUser):
    professional_license = models.CharField(max_length=50, unique=True)
    institution = models.CharField(max_length=200, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
    
    # Hacer email único y requerido
    email = models.EmailField(unique=True)
    
    # Usar email como username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # username sigue siendo requerido por AbstractUser

    class Meta:
        verbose_name = 'Psychologist'
        verbose_name_plural = 'Psychologists'

    def __str__(self):
        return f"{self.get_full_name()} - {self.professional_license}"

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)