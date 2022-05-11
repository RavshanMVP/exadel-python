from rest_framework import serializers
import sys
sys.path.append("....")
from core.models.service import Service
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'cost','company_id']

