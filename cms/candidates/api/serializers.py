from rest_framework import serializers

from ..models import CandidateModel


class CandidateSerializer(serializers.ModelSerializer):

    # author_name = serializers.SerializerMethodField('get_author')
    class Meta:
        model  = CandidateModel
        fields = ('id', 'name', 'email', 'date', 'contact', 'resume', 'job_applied_to')

    # def get_author(self, Article):
    #     return Article.author.username