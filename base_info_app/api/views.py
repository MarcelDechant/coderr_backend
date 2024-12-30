from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Avg
from profile_app.models import Profile
from .serializers import BaseInfoSerializer
from rest_framework.permissions import AllowAny

class BaseInfoView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        review_count = 0
        average_rating = 0
        business_profile_count = Profile.objects.filter(type='business').count()
        offer_count = 0

        data = {
            "review_count": review_count,
            "average_rating": average_rating,
            "business_profile_count": business_profile_count,
            "offer_count": offer_count,
        }

        serializer = BaseInfoSerializer(data)
        return Response(serializer.data)