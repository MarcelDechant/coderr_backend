from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from profile_app.models import Profile
from offers_app.models import Offer
from reviews_app.models import Review


class BaseInfoViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('base-info')

        Profile.objects.create(user=1, username="Business1", type="business")
        Profile.objects.create(user=2, username="Business2", type="business")
        
        Offer.objects.create(title="Test Offer 1", description="Test description")
        Offer.objects.create(title="Test Offer 2", description="Test description")
        
        Review.objects.create(business_user=1, reviewer=101, rating=4, description="Great service!")
        Review.objects.create(business_user=2, reviewer=102, rating=3, description="Good experience!")

    def test_get_base_info(self):

        response = self.client.get(self.url)
        
        
        ratings = [4.5, 3.5]  
        calculated_average = sum(ratings) / len(ratings)
  
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        expected_data = {
            "review_count": 2,
            "average_rating": 3.5,
            "business_profile_count": 2,
            "offer_count": 2,
        }
        self.assertEqual(response.data, expected_data)

    def test_get_base_info_no_data(self):

        Profile.objects.all().delete()
        Offer.objects.all().delete()
        Review.objects.all().delete()
        
        response = self.client.get(self.url)
        
        expected_data = {
            "review_count": 0,
            "average_rating": 0.0,
            "business_profile_count": 0,
            "offer_count": 0,
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)