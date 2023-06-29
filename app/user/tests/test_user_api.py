# Test the userApi.
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase

# url endpoint for creating user and generating token
CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    # Create and return a new user.
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    # Test the public feature of the user Api.

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        # Test creating a user is successful.
        payload = {
            'email': 'test@example.com',
            'name': 'Test Name',
            'password': 'testpass123'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        # Don't create user if email already exist in database.
        payload = {
            'email': 'test@example.com',
            'name': 'Test Name',
            'password': 'testpass123'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        payload = {
            'email': 'test@example.com',
            'name': 'Test Name',
            'password': 'te'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload[
                'email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        # Test to generate token for valid credentials.
        user_details = {'name': 'Test name',
                        'email': 'test@example.com',
                        'password': 'test-user-password123'}
        create_user(**user_details)
        payload = {'email': user_details['email'],
                   'password': user_details['password']}
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        # Test to return error if credentials is invalid.
        create_user(email='test@example.com', password='goodpass')
        payload = {'email': 'test@example.com', 'password': 'badpass'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        # Test to return error if password is blank.
        payload = {'email': 'test@example.com', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrive__user_unauthorized(self):
        # Test authentication is required for users.
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    # Test API requests that requires authentication
    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='testpass123',
            name='Test Name'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrive_profile_success(self):
        # Test Retriving Profile for authenticated user(loggedin user)
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {'name': self.user.name,
                                    'email': self.user.email,
                                    })

    def test_post_me_not_allowed(self):
        # Test POST is not allowed for the me endpoint
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        # Test updating the user profile for the authenticated user
        payload = {'name': 'Updated name', 'password': 'newpassword123'}
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()  # Refresh user value from db since it's not refresh authomatically
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
