# from rest_framework.test import APITestCase
# from rest_framework import status
# from django.contrib.auth.models import User

# class CustomLoginViewTests(APITestCase):

#     def setUp(self):
#         # Erstelle einen Testbenutzer
#         self.user = User.objects.create_user(username='testuser', password='testpassword123')
#         self.url = '/api/login/'  # Die URL des Login-Endpunkts

#     def test_login_successful(self):
#         # Teste, ob der Login erfolgreich ist
#         data = {
#             'username': 'testuser',
#             'password': 'testpassword123'
#         }
#         response = self.client.post(self.url, data, format='json')

#         # Überprüfen, ob der Status Code 200 OK ist
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         # Überprüfen, ob das Token im Antwort-Body enthalten ist
#         self.assertIn('token', response.data)

#         # Überprüfen, ob der Benutzername, die E-Mail und die User-ID in der Antwort enthalten sind
#         self.assertEqual(response.data['username'], 'testuser')
#         self.assertEqual(response.data['email'], self.user.email)
#         self.assertEqual(response.data['user_id'], self.user.id)

#     def test_login_invalid_credentials(self):
#         # Teste, ob bei falschen Anmeldedaten ein Fehler zurückgegeben wird
#         data = {
#             'username': 'testuser',
#             'password': 'wrongpassword'
#         }
#         response = self.client.post(self.url, data, format='json')

#         # Überprüfen, ob der Status Code 400 Bad Request ist
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#         # Überprüfen, ob die Fehlermeldung korrekt ist
#         self.assertIn('detail', response.data)
#         self.assertEqual(response.data['detail'][0], 'Ungültiger Benutzername oder Passwort.')

#     def test_login_missing_fields(self):
#         # Teste, ob bei fehlenden Feldern ein Fehler zurückgegeben wird
#         data = {
#             'username': 'testuser'
#         }
#         response = self.client.post(self.url, data, format='json')

#         # Überprüfen, ob der Status Code 400 Bad Request ist
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#         # Überprüfen, ob die Fehlermeldung korrekt ist
#         self.assertIn('password', response.data)
#         self.assertEqual(response.data['password'][0], 'This field is required.')
