from django import forms
from django.core.exceptions import ValidationError

from . import models


class CreateCandidateForm(forms.ModelForm):
    """
        Candidate Creation Form that allows creation of candidates through the UI.
    """
    class Meta:
        model = models.CandidateModel
        fields = '__all__'