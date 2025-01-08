from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from profile_app.models import Profile

class RegistrationViewTest(APITestCase):
    def setUp(self):
        self.registration_url = '/api/registration/' 

    def test_successful_registration(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'securepassword',
            'repeated_password': 'securepassword'
        }
        response = self.client.post(self.registration_url, data, format='json')
        self.assertEqual(response.status_code, 200)  
        self.assertIn('username', response.data) 

    def test_password_mismatch(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'securepassword',
            'repeated_password': 'differentpassword'
        }
        response = self.client.post(self.registration_url, data, format='json')
        self.assertEqual(response.status_code, 400)  
        self.assertIn('password', response.data)  
        self.assertEqual(
            response.data['password'][0],
            'Das Passwort ist nicht gleich mit dem wiederholten Passwort'  
        )

    def test_duplicate_email(self):
        """Testet, ob ein Fehler für doppelte E-Mail-Adressen geworfen wird."""
        User.objects.create_user(username='existinguser', email='testuser@example.com', password='password123')

        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'securepassword123',
            'repeated_password': 'securepassword123'
        }

        response = self.client.post(self.registration_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'][0], "Diese E-Mail-Adresse wird bereits verwendet.")

    def test_duplicate_username(self):
        """Testet, ob ein Fehler für doppelte Benutzernamen geworfen wird."""

        User.objects.create_user(username='testuser', email='other@example.com', password='password123')

        data = {
            'username': 'testuser',
            'email': 'newuser@example.com',
            'password': 'securepassword123',
            'repeated_password': 'securepassword123'
        }


        response = self.client.post(self.registration_url, data, format='json')


        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


        self.assertIn('username', response.data)


        self.assertEqual(response.data['username'][0], "A user with that username already exists.")

    def test_profile_creation(self):
        """Testet, ob ein Profil korrekt erstellt wird."""

        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'securepassword123',
            'repeated_password': 'securepassword123',
            'type': 'customer'
        }


        response = self.client.post(self.registration_url, data, format='json')


        self.assertEqual(response.status_code, status.HTTP_200_OK)


        profile_exists = Profile.objects.filter(username='testuser').exists()
        self.assertTrue(profile_exists, "Profil wurde nicht erstellt.")


        profile = Profile.objects.get(username='testuser')
        self.assertEqual(profile.type, 'customer', "Der Typ des Profils ist nicht korrekt.")
        self.assertEqual(profile.first_name, 'Testuser', "Der Vorname des Profils ist nicht korrekt.")

