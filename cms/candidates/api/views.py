from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.auth.models import User
import os

from ..models import CandidateModel
from .serializers import CandidateSerializer


@permission_classes((IsAuthenticated,))
class CandidateAPIView(APIView):

    def get(self, request, id=None):
        if id is not None:
            try:
                candidate = CandidateModel.objects.get(id=id)
            except CandidateModel.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = CandidateSerializer(candidate)
            return Response(serializer.data)

        candidates = CandidateModel.objects.all()
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data)

    def post(self, request):
        candidate  = CandidateModel()
        serializer = CandidateSerializer(candidate, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            candidate = CandidateModel.objects.get(id=id)
        except CandidateModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CandidateSerializer(candidate, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            candidate = CandidateModel.objects.get(id=id)
        except CandidateModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if os.path.isfile(candidate.resume.path):
            os.remove(candidate.resume.path)
        candidate.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
