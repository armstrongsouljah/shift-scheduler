from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from authentication.models import User
from .views import UserProfileListView, UserProfileUpdateView


# Create your tests here.
class TestUserProfile(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_user = User.objects.create(
            email='samplemail@gmail.com',
            username='sampleuser',
            password='password123')
    
    def test_fetching_user_profiles_when_logged_out_fails(self):
        response = self.client.get('/profiles/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_fetching_user_profiles_when_logged_in_returns_profile_list(self):

        self.client.login(username=self.test_user.email, password=self.test_user.password)
        response = self.client.get('/profiles/',
        content_type='application/json',
        HTTP_AUTHORIZATION='Bearer ' + self.test_user.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def testing_updating_a_profile_when_logged_out_fails(self):
        response = self.client.get('/profiles/update')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    

