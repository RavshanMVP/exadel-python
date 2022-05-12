from rest_framework import serializers
import sys
sys.path.append("....")
from core.models import RequestStatus
class RequestStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestStatus
        fields = [ 'status']

