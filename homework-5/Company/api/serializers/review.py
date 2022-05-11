from rest_framework import serializers
import sys
sys.path.append("....")
from core.models.review import Review
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['rating', 'feedback', 'created_at','request_id ','user_id','service_id']

        request_id = serializers.SerializerMethodField()
        user_id = serializers.SerializerMethodField()
        service_id = serializers.SerializerMethodField()

        def get_user(self,review):
            return review.user_id.fullname
        def get_service(self,review):
            return review.service_id.role
        def get_request(self,review):
            return review.request_id.role
