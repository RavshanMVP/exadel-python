from rest_framework import serializers
import sys
sys.path.append("....")
from core.models.request_status import RequestStatus
class RequestStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestStatus
        fields = [ 'status']

