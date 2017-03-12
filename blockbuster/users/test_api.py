from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User


class UserViewTestCase(APITestCase):
    def test__create_user_is_successful(self):
        # GIVEN a request to create a new user with the required fields
        username = 'testuser'
        password = 'blockbuster'
        email = 'blockbuster@test.com'
        data = dict(
            username=username,
            password=password,
            email=email
        )
        url = 'http://127.0.0.1:8000/api/register/'
        # WHEN the request is made
        response = self.client.post(url, data, format='json')
        user = User.objects.get(username=username)
        # THEN the user is in the system
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.email, email)
        # AND they have a profile
        self.assertTrue(user.profile)

    def test__create_user_with_invalid_email_fails(self):
        # GIVEN a request to create a new user but the email is invalid
        username = 'testuser'
        password = 'blockbuster'
        email = 'blockbustersss'
        data = dict(
            username=username,
            password=password,
            email=email
        )
        url = 'http://127.0.0.1:8000/api/register/'
        # WHEN the request is made
        response = self.client.post(url, data, format='json')

        # THEN the error message is displayed
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("email")[0], "Enter a valid email address.")

    def test__create_user_with_missing_required_field_fails(self):
        # GIVEN a request to create a new user but the request doesnt contain some needed info
        password = 'blockbuster'
        email = 'blockbusters@test.com'
        data = dict(
            password=password,
            email=email
        )
        url = 'http://127.0.0.1:8000/api/register/'
        # WHEN the request is made
        response = self.client.post(url, data, format='json')

        # THEN the error message is displayed
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("username")[0], "This field is required.")