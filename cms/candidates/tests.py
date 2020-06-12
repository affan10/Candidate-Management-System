from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import CandidateModel
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime


class CandidateAPITests(APITestCase):

    def setUp(self):
        """
            This method sets up test data before every unit test is called.
        """
        CandidateModel.objects.create(name='Test Candidate', email='test@email.com',
                                      date=datetime.now(), contact='123456789',
                                      resume=SimpleUploadedFile("testfile.pdf", b"Python Java"),
                                      job_applied_to='Backend Engineer')

        User.objects.create_user(username='testuser123', password='testpass123',
                                 email='django_test@example.com', is_superuser=True, is_staff=True)

    def test_signup_endpoint(self):
        """
            Test checks if signup endpoint is working correctly, both when correct and incorrect
            credentials are provided.
        """
        data     = {"username": "test_user123", "password": "testpass123",
                    "confirm_password": "testpass123"}
        url = "/api/accounts/signup/"
        response = self.client.post(url, data=data)

        # When correct credentials are provided
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # When incorrect credentials provided i.e. passwords do not match
        data["confirm_password"] = "changedPass"
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_endpoint(self):
        """
            Test checks if login endpoint is working correctly, both when correct and incorrect
            credentials are provided.
        """
        url   = "/api/accounts/login/"
        data  = {'username': 'testuser123', 'password': 'testpass123'}
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # For incorrect password provided by the client
        data["password"] = "changedPass"
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # For incorrect username provided by the client
        data["username"] = "changedUser"
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)