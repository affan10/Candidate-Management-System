from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import SignupAPIView

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup-api-view'),
    path('login/', obtain_auth_token, name='login-api-view'),
]