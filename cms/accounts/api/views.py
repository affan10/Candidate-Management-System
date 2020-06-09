from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from .serializers import SignupSerializer


@authentication_classes([])
@permission_classes([])
class SignupAPIView(APIView):
    """
        This class handles user requests to signup to the system and become an admin user.
    """
    def post(self, request):
        """
            This method handles requests for users to signup.

            :param request: standard request object that contains details about the request received.
            :return: the newly created username and auth_token in case of success
                    - HTTP 400 Bad Request Error code in case of error.
        """
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user         = serializer.save()
            data_to_send = {
                'username': serializer.data['username'],
                'auth_token': Token.objects.get(user=user).key
            }
            return Response(data_to_send, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
