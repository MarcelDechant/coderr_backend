from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.contrib.auth import get_user_model
from offers_app.models import OfferDetail
from orders_app.models import Order
from profile_app.models import Profile

class OrderTests(APITestCase):

    def setUp(self):
        self.business_user = get_user_model().objects.create_user(
            username="business_user", password="password123")
        self.customer_user = get_user_model().objects.create_user(
            username="customer_user", password="password123")
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
        
        self.token = Token.objects.create(user=self.customer_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.offer_detail = OfferDetail.objects.create(
            user=self.business_user.id,
            title="Premium",
            revisions=1,
            delivery_time_in_days=7,
            price=Decimal('20.00'),
            features={},
            offer_type="premium"
        )
      
        self.order_data = {
            "offer_detail_id": self.offer_detail.id
        }
        
        self.order_url = reverse('orders:order-list') 
        
        self.order = Order.objects.create(
            customer_user=self.customer_user.id,
            business_user=self.business_user.id,
            title=self.offer_detail.title,
            revisions=1,
            delivery_time_in_days=7,
            price=self.offer_detail.price,
            features=self.offer_detail.features,
            offer_type=self.offer_detail.offer_type,
            status="in_progress"
        )

    def test_create_order(self):
        self.client.login(username='customer_user', password='password123')
        response = self.client.post(self.order_url, self.order_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], self.offer_detail.title)
        self.assertEqual(str(response.data['price']), str(self.offer_detail.price))

    def test_get_orders(self):

        self.client.login(username='customer_user', password='password123')
        url = reverse('orders:order-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.order.title)

    def test_order_count_in_progress(self):

        url = reverse('order-count:order-count', args=[self.business_user.id])
        self.client.login(username='business_user', password='password123')
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['order_count'], 1)

    def test_completed_order_count(self):

        self.order.status = 'completed'
        self.order.save()
        
        url = reverse('completed-order-count:completed-order-count', args=[self.business_user.id])
        self.client.login(username='business_user', password='password123')
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['completed_order_count'], 1)

    def test_permission_is_customer(self):

        url = reverse('orders:order-list')
        self.client.login(username='customer_user', password='password123')
        response = self.client.post(url, self.order_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_permission_is_owner_or_admin(self):

        self.client.login(username='business_user', password='password123')
        
        url = reverse('orders:order-detail', kwargs={'pk': self.order.id})
        response = self.client.patch(url, {'status': 'completed'}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        

        self.client.login(username='customer_user', password='password123')
        response = self.client.patch(url, {'status': 'completed'}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)