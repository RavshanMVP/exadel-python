from rest_framework import serializers
import sys
sys.path.append("....")
from core.models.review import Review
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'rating', 'feedback', 'created_at','request_id ','user_id','service_id']
