from rest_framework import serializers
import sys
sys.path.append("....")
from core.models.service import Service
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [ 'name', 'cost','company_id']

        company_id = serializers.SerializerMethodField()

        def get_role(self,service):
            return service.company_id.fullname

