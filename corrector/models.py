from django.db import models

# Create your models here.
from django.db import models

class Correction(models.Model):
    original_sentence = models.TextField()
    corrected_sentence = models.TextField()
    explanation = models.TextField()
    difficulty = models.CharField(max_length=10, blank=True, null=True)
    confidence = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.original_sentence[:50]} ➔ {self.corrected_sentence[:50]}"

