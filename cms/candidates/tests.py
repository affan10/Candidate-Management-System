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
                                      job_applied_to='Backend Engineer'
                                      #resume=SimpleUploadedFile("testfile.pdf", b"Python Java")
                                     )

        User.objects.create_user(username='test123', password='test@123',
                                 email='test@user.com', is_superuser=True, is_staff=True)

    def test_signup_endpoint(self):
        """
            Test checks if signup endpoint is working correctly, both when correct and incorrect
            credentials are provided.
        """
        data     = {"username": "test_user123", "password": "testpass123",
                    "confirm_password": "testpass123"}
        url = reverse('account_signup_api:signup-api-view')
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
        url = reverse('account_signup_api:login-api-view')
        data  = {'username': 'test123', 'password': 'test@123'}
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

    def test_viewing_all_candidates(self):
        """
            Test checks whether a user can successfully view all candidates if correct
            credentials are provided and receives an error otherwise.
        """
        token = Token.objects.get(user__username='test123')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url      = reverse('candidates_api:candidates-list-and-post-apiurl')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # for incorrect authorization i.e. the client uses an invalid or someone else's token
        self.client.credentials(HTTP_AUTHORIZATION='Token 12345invalidtoken')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_viewing_specific_candidate(self):
        """
            Test checks whether a user can successfully view a specific candidates if
            correct credentials are provided and receives an error otherwise.
        """
        token     = Token.objects.get(user__username='test123')
        candidate = CandidateModel.objects.get(name='Test Candidate')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url      = reverse('candidates_api:get-apiurl', args=[candidate.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # If candidate whose ID requested in the URL is not present in the database
        url = reverse('candidates_api:get-apiurl', args=[12345])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_creating_new_candidate(self):
        """
            Test to check if a new candidate is being created successfully given
            correct parameters are being sent by an authorized client.
        """
        # Creating test file
        path = '/home/affan/qatask/cms/testCasesFileUploads/testUploadFile.docx'
        file = open(path, 'w+')
        file.write('Python Java SQL\n')
        file.close()
        file = open(path, 'rb')

        token = Token.objects.get(user__username='test123')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url  = reverse('candidates_api:candidates-list-and-post-apiurl')
        data = {'name': 'anotherTestCand', 'email': 'testapi@testcand.com', 'contact': '1234567',
                'resume': file,
                'job_applied_to': 'ML Engineer'}
        response = self.client.post(url, data, format='multipart')
        file.close()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # To check if the client tries to upload file with disallowed extensions
        # Only allowed extensions are .docx and .pdf
        path = '/home/affan/qatask/cms/testCasesFileUploads/testUploadFile.xls'
        file = open(path, 'w+')
        file.write('Python Java SQL\n')
        file.close()
        file = open(path, 'rb')
        data['resume'] = file
        response = self.client.post(url, data, format='multipart')
        file.close()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)