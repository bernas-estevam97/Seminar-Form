from django.db import models


class SeminarFormModel(models.Model):
    seminar_title = models.CharField(max_length=100)
    seminar_speaker = models.CharField(max_length=50)
    seminar_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title