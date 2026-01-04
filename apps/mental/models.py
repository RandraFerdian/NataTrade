from django.db import models
from django.contrib.auth.models import User

class MentalAudit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vision_score = models.IntegerField() # Skor emosi dari AI Vision
    nlp_score = models.IntegerField() # Skor disiplin dari NLP
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def combined_score(self):
        # Rata-rata dari Vision dan NLP
        return (self.vision_score + self.nlp_score) / 2