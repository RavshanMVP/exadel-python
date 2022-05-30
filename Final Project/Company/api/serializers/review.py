from rest_framework import serializers
from core.models import Review
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [ 'id', 'rating', 'feedback', 'created_at','request','user','service']

    request = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    service = serializers.SerializerMethodField()

    def get_user(self,review):
        return review.user.fullname
    def get_service(self,review):
        return review.service.name
    def get_request(self,review):
        return review.request.id
