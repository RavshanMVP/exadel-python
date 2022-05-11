from rest_framework import serializers
import sys
sys.path.append("....")
from core.models.request import Request
class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['id', 'address', 'created_at', 'area','cost_total','status_id','user_id','service_id']


