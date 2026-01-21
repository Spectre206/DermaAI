from django.db import models
from django.conf import settings
# Create your models here.

class SkinLesionScan(models.Model):
    '''
    Stores the history of AI scans for the patients
    '''
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, related_name='scans')

    # The Scanned Image
    image = models.ImageField(upload_to='lesion_scans/%Y/%m/%d/')
    heatmap_image = models.CharField(max_length=255, blank=True, null=True)

    # AI Results (Saved after prediction)
    prediction = models.CharField(max_length=100, blank=True)
    confidence = models.FloatField(default=0.0)
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.patient} - {self.prediction} ({self.confidence}%)"

class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    rating = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.subject}"