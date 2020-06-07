from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from .serializers import SignupSerializer


@authentication_classes([])
@permission_classes([])
class SignupAPIView(APIView):

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user         = serializer.save()
            data_to_send = {
                'username': serializer.data['username'],
                'auth_token': Token.objects.get(user=user).key
            }
            return Response(data_to_send, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)