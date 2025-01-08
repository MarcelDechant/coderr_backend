from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from offers_app.models import Offer, OfferDetail
from profile_app.models import Profile
from decimal import Decimal
from rest_framework.authtoken.models import Token

class OfferModelTest(TestCase):

    def setUp(self):
        self.profile = Profile.objects.create(user=1, username="business_user", type="business")

    def test_create_offer(self):
        offer = Offer.objects.create(
            user=self.profile.user,
            title="Test Offer",
            description="Test Description",
            min_price=Decimal('10.00'),
            max_delivery_time=30,
            min_delivery_time=10
        )

        self.assertEqual(offer.title, "Test Offer")
        self.assertEqual(offer.description, "Test Description")
        self.assertEqual(offer.min_price, Decimal('10.00'))
        self.assertEqual(offer.max_delivery_time, 30)
        self.assertEqual(offer.min_delivery_time, 10)

    def test_create_offer_with_details(self):
        details_data = [
            {'title': 'Basic', 'revisions': 1, 'delivery_time_in_days': 5, 'price': float(Decimal('10.00')), 'features': {}, 'offer_type': 'basic'},
            {'title': 'Standard', 'revisions': 1, 'delivery_time_in_days': 10, 'price': float(Decimal('15.00')), 'features': {}, 'offer_type': 'standard'},
            {'title': 'Premium', 'revisions': 1, 'delivery_time_in_days': 7, 'price': float(Decimal('20.00')), 'features': {}, 'offer_type': 'premium'}
        ]
        offer = Offer.objects.create(
            user=self.profile.user,
            title="Test Offer With Details",
            description="Test Description",
            min_price=Decimal('10.00'),
            max_delivery_time=30,
            min_delivery_time=5
        )
        offer.details = details_data  
        offer.save()

        self.assertEqual(len(offer.details), 3)  
        self.assertEqual(offer.min_price, Decimal('10.00'))
        self.assertEqual(offer.min_delivery_time, 5)

    def test_offer_detail_creation(self):
        offer_detail = OfferDetail.objects.create(
            user=self.profile.user,
            title="Premium",
            revisions=1,
            delivery_time_in_days=7,
            price=Decimal('20.00'),
            features={},
            offer_type='premium'
        )

        self.assertEqual(offer_detail.title, "Premium")
        self.assertEqual(offer_detail.price, Decimal('20.00'))
        self.assertEqual(offer_detail.delivery_time_in_days, 7)


class OfferViewSetTest(TestCase):

    def setUp(self):
        self.client = APIClient()

        user = get_user_model().objects.create_user(
            username="business_user", password="password123")
        self.profile = Profile.objects.create(
            user=user.id, username="business_user", type="business")

        self.offer = Offer.objects.create(
            user=self.profile.user,
            title="Test Offer",
            description="Test Description",
            min_price=float(Decimal('10.00')),
            max_delivery_time=30,
            min_delivery_time=10
        )

        self.offer_detail = OfferDetail.objects.create(
            user=self.profile.user,
            title="Premium",
            revisions=1,
            delivery_time_in_days=7,
            price=float(Decimal('20.00')),
            features={},
            offer_type="premium"
        )

        self.url = reverse('offers:offer-list')
        self.url_detail = reverse(
            'offers:offer-detail', kwargs={'pk': self.offer.pk})

        self.token = Token.objects.create(user=user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_offers(self):
        response = self.client.get(self.url)


        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], "Test Offer")

    def test_create_offer(self):
        details_data = [
            {"title": "Basic", "offer_type": "basic", "price": 10.00, "delivery_time_in_days": 7,
            "features": {"description": "Basic features of the offer, ideal for small needs."}, "revisions": 1},
            {"title": "Standard", "offer_type": "standard", "price": 15.00, "delivery_time_in_days": 10, "features": {
                "description": "Standard features, providing a balanced offer with more options."}, "revisions": 1},
            {"title": "Premium", "offer_type": "premium", "price": 20.00, "delivery_time_in_days": 15, "features": {
                "description": "Premium features with full support and fast delivery time."}, "revisions": 1}
        ]

        offer_data = {
            "title": "New Offer",
            "description": "New Description",
            "min_price": float(Decimal('15.00')),
            "max_delivery_time": 25,
            "min_delivery_time": 10,
            "user": self.profile.user,
            "details": details_data
        }

        response = self.client.post(self.url, offer_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "New Offer")
        self.assertEqual(len(response.data['details']), 3)


