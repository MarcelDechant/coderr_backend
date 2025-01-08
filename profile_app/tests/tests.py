from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from profile_app.models import Profile
from django.contrib.auth.models import User
from profile_app.api.serializers import ProfileSerializer

class ProfileModelTest(TestCase):
    def setUp(self):
        self.profile = Profile.objects.create(
            user=1,
            username="testuser",
            first_name="Test",
            last_name="User",
            email="testuser@example.com",
            type="customer"
        )

    def test_profile_creation(self):
        self.assertEqual(self.profile.username, "testuser")
        self.assertEqual(self.profile.type, "customer")
        self.assertIsNotNone(self.profile.created_at)

class ProfileViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.profile = Profile.objects.create(
            user=self.user.id,
            username="testuser",
            first_name="Test",
            last_name="User",
            email="testuser@example.com",
            type="customer"
        )
        self.client.force_authenticate(user=self.user)
        self.detail_url = reverse('profile-detail', kwargs={"pk": self.user.id})
        self.customer_list_url = reverse('customer-list')

    def test_get_profile(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], "testuser")

    def test_patch_profile(self):
        data = {"first_name": "Updated"}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], "Updated")

    def test_get_customer_profiles(self):
        response = self.client.get(self.customer_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_permission_denied(self):
        other_user = User.objects.create_user(username="otheruser", password="password123")
        other_client = APIClient()
        other_client.force_authenticate(user=other_user)
        response = other_client.patch(self.detail_url, {"first_name": "Unauthorized"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class ProfileSerializerTest(TestCase):
    def setUp(self):
        self.profile_data = {
            "user": 1,
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@example.com",
            "type": "customer",
        }

    def test_serializer_valid(self):
        serializer = ProfileSerializer(data=self.profile_data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_invalid(self):
        invalid_data = self.profile_data.copy()
        invalid_data["email"] = "not-an-email"
        serializer = ProfileSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())