from django.db import models
from django.core.validators import FileExtensionValidator
import os

# Create your models here.


def rename_and_save(instance, filename):
    path   = "media/"
    format = f'{instance.email}_{filename}'
    return os.path.join(path, format)


class CandidateModel(models.Model):
    name           = models.CharField(max_length=100)
    email          = models.EmailField()
    date           = models.DateTimeField(auto_now_add=True)
    contact        = models.CharField(max_length=13)
    resume         = models.FileField(upload_to=rename_and_save, validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])], null=True, blank=True)
    job_applied_to = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name} -- {self.email}'