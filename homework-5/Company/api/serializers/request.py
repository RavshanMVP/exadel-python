from rest_framework import serializers
import sys
sys.path.append("....")
from core.models.request import Request
sys.path.clear()
class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = [ 'address', 'created_at', 'area','cost_total','status_id','user_id','service_id']

        status_id = serializers.SerializerMethodField()
        user_id = serializers.SerializerMethodField()
        service_id = serializers.SerializerMethodField()

        def get_status(self, requests):
            return requests.status_id.status

        def get_user(self, requests):
            return requests.user_id.fullname

        def get_service(self, requests):
            return requests.service_id.name


