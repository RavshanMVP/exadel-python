from rest_framework import serializers
import sys
sys.path.append("....")
from core.models import Service
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [ 'id', 'name', 'cost','company']

        company = serializers.SerializerMethodField()

        def get_company(self,service):
            return service.company.fullname

