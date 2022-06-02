from rest_framework import serializers
from core.models import RequestStatus
class RequestStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestStatus
        fields = ['id', 'status']

