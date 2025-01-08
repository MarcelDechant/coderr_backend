from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from reviews_app.models import Review
from django.contrib.auth import get_user_model
from profile_app.models import Profile

class ReviewTests(APITestCase):

    def setUp(self):
        self.business_user = get_user_model().objects.create_user(
            username="business_user", password="password123")
        self.customer_user = get_user_model().objects.create_user(
            username="customer_user", password="password123")
        self.other_user = get_user_model().objects.create_user(
            username="other_user", password="password123")

        self.business_profile = Profile.objects.create(
            user=self.business_user.id,
            username="business_user",
            first_name="Business",
            last_name="User",
            type="business",
            email="business@example.com"
        )
        
        self.customer_profile = Profile.objects.create(
            user=self.customer_user.id,
            username="customer_user",
            first_name="Customer",
            last_name="User",
            type="customer",
            email="customer@example.com"
        )
        
        self.other_profile = Profile.objects.create(
            user=self.other_user.id,
            username="other_user",
            first_name="Other",
            last_name="User",
            type="customer",
            email="other@example.com"
        )
        
        self.customer_token = Token.objects.create(user=self.customer_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        

        self.review = Review.objects.create(
            business_user=self.business_user.id,
            reviewer=self.other_user.id,
            rating=5,
            description="Excellent service!"
        )

        self.review_url = f"/api/reviews/{self.review.id}/"
        self.review_list_url = "/api/reviews/"

    def test_create_review(self):
        """Testet das Erstellen einer Bewertung durch einen Kunden."""
        data = {
            "business_user": self.business_user.id,
            "rating": 4,
            "description": "Great!"
        }
        
        response = self.client.post(self.review_list_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 2)
        self.assertEqual(Review.objects.last().rating, 4)


    def test_get_review_list(self):
        """Testet das Abrufen der Bewertungen."""
        
        response = self.client.get(self.review_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_single_review(self):
        """Testet das Abrufen einer einzelnen Bewertung."""
        
        response = self.client.get(self.review_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["description"], self.review.description)

    def test_update_review(self):
        """Testet das Aktualisieren einer Bewertung durch den Bewerter."""
        other_user_token = Token.objects.create(user=self.other_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {other_user_token.key}')
        
        update_data = {
            "rating": 4,
            "description": "Updated review"
        }
        
        response = self.client.patch(self.review_url, update_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.review.refresh_from_db()
        self.assertEqual(self.review.rating, 4)
        self.assertEqual(self.review.description, "Updated review")

    def test_delete_review(self):
        """Testet das Löschen einer Bewertung durch den Bewerter."""
        other_user_token = Token.objects.create(user=self.other_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {other_user_token.key}')
        
        response = self.client.delete(self.review_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Review.objects.count(), 0)



    def test_permission_denied_for_non_reviewer(self):
        """Testet, dass ein anderer Benutzer eine Bewertung nicht aktualisieren oder löschen kann."""
        self.customer_token = Token.objects.get(user=self.customer_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        
        update_data = {
            "rating": 3,
            "description": "Not allowed"
        }
        response = self.client.patch(self.review_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.delete(self.review_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



    def test_cannot_leave_multiple_reviews_from_same_user(self):
        """Testet, dass derselbe Benutzer nicht mehrere Bewertungen für denselben Business-Benutzer hinterlassen kann."""
    
        data = {
            "business_user": self.business_user.id,
            "rating": 4,
            "description": "Duplicate review attempt"
        }
    
        other_user_token = Token.objects.create(user=self.other_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {other_user_token.key}')
        
        response = self.client.post(self.review_list_url, data)
    
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("You can only leave one review per business user.", str(response.data))