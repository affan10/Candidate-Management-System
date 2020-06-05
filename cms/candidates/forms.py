from django import forms
from django.core.exceptions import ValidationError

from . import models


class CreateCandidateForm(forms.ModelForm):
    class Meta:
        model = models.CandidateModel
        fields = '__all__'