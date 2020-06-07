from rest_framework import serializers

from ..models import CandidateModel


class CandidateSerializer(serializers.ModelSerializer):
    """
        This serializer is responsible for serializing the Candidate Model.
    """
    class Meta:
        model  = CandidateModel
        fields = ('id', 'name', 'email', 'date', 'contact', 'resume', 'job_applied_to')