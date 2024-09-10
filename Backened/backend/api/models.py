from django.db import models

class Document(models.Model):
    resume = models.FileField(upload_to='resumes/')
    job_description = models.FileField(upload_to='job_descriptions/')


