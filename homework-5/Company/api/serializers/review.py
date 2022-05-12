from rest_framework import serializers
import sys
sys.path.append("....")
from core.models.review import Review
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['rating', 'feedback', 'created_at','request ','user','service']

        request = serializers.SerializerMethodField()
        user = serializers.SerializerMethodField()
        service = serializers.SerializerMethodField()

        def get_user(self,review):
            return review.user.fullname
        def get_service(self,review):
            return review.service.role
        def get_request(self,review):
            return review.request.role
