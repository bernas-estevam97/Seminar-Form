from django.db import models
from django.contrib.auth.models import User


class SeminarFormModel(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)  # Explicitly defining ID
    seminar_title = models.CharField(max_length=100)
    seminar_speaker = models.CharField(max_length=50)
    seminar_date = models.DateField(blank=True, null=True)
    verification_id = models.CharField(blank=False, null=False, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{str(self.user) + ": " + str(self.seminar_title)}'
    

class WordDocument(models.Model):
    name = models.CharField(max_length=100)  # File name or metadata
    file = models.FileField(upload_to='generated_reports/')  # Folder in MEDIA_ROOT
    created_at = models.DateTimeField(auto_now_add=True)