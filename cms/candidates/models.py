from django.db import models
from django.core.validators import FileExtensionValidator
import os

# Create your models here.


def rename_and_save(instance, filename):
    path   = "media/"
    format = f'{instance.email}_{filename}'
    return os.path.join(path, format)


class CandidateModel(models.Model):
    JOBS = (
        ('Backend Engineer', 'Backend Engineer'),
        ('Frontend Engineer', 'Frontend Engineer'),
        ('Python Developer', 'Python Developer'),
        ('Business Analyst', 'Business Analyst'),
        ('ML Engineer', 'ML Engineer'),
        ('Data Engineer', 'Data Engineer'),
        ('Technical Recruiter', 'Technical Recruiter'),
    )

    name           = models.CharField(max_length=100)
    email          = models.EmailField()
    date           = models.DateTimeField(auto_now_add=True)
    contact        = models.CharField(max_length=13, blank=True)
    resume         = models.FileField(upload_to=rename_and_save, validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])], null=True)
    job_applied_to = models.CharField(max_length=100, choices=JOBS)

    def __str__(self):
        return f'{self.name} -- {self.email}'