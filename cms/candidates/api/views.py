from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
import os

from ..models import CandidateModel
from .serializers import CandidateSerializer


@permission_classes((IsAuthenticated,))
class CandidateAPIView(APIView):
    """
        - This class handles all GET / POST / PUT / DELETE requests and returns appropriate
          responses through the Django REST Framework.
        - All methods defined below require an authenticated request i.e. User must be logged-in
          to access these methods.
        - Once an authenticated request is received, they appropriately handle them based on
          validations present in the system and return appropriate HTTP Status Codes and
          JSON Responses.
    """

    def get(self, request, id=None):
        """
            This method handles GET requests to:
            - Get all candidates.
            - Get a specific candiate.

            :param request: standard request object that contains details about the request received.
            :param id: id of the candidate. Is initialized to None if no id is present in the request.
            :return: list of candidates or a single candidate based on the GET request.
                    - HTTP 404 Not Found Error Code in case of failure.
        """
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
        """
            This method handles POST requests to add new candidates.
            :param request: standard request object that contains details about the request received.
            :return: newly created Candidate object in case of success.
                    - HTTP 400 Bad Request Code in case of failure.
        """
        candidate  = CandidateModel()
        serializer = CandidateSerializer(candidate, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        """
            This method handles PUT requests to update a specific candidate.

            :param request: standard request object that contains details about the request received.
            :param id: id of the candidate to be updated.
            :return: updated candidate in case of success.
                    - HTTP 404 Not Found Error Code in case candidate with the id requested is not found.
                    - HTTP 400 Bad Request Error Code in case of failure.
        """
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
        """
            This method handles DELETE requests to delete a specific candidate.

            :param request: standard request object that contains details about the request received.
            :param id: id of the candidate to be deleted.
            :return: HTTP 204 No Content Status Code on successful deletion.
                    - HTTP 404 Not Found Error Code in case candidate with the id requested is not found.
        """
        try:
            candidate = CandidateModel.objects.get(id=id)
        except CandidateModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if os.path.isfile(candidate.resume.path):
            os.remove(candidate.resume.path)
        candidate.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
