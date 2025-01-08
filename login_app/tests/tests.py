from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class CustomLoginViewTests(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.url = '/api/login/' 

    def test_login_successful(self):
      
        data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        response = self.client.post(self.url, data, format='json')


        self.assertEqual(response.status_code, status.HTTP_200_OK)


        self.assertIn('token', response.data)


        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['user_id'], self.user.id)

    def test_login_invalid_credentials(self):

        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.url, data, format='json')

  
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'][0], 'Ungültiger Benutzername oder Passwort.')

    def test_login_missing_fields(self):

        data = {
            'username': 'testuser'
        }
        response = self.client.post(self.url, data, format='json')


        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn('password', response.data)
        self.assertEqual(response.data['password'][0], 'This field is required.')
