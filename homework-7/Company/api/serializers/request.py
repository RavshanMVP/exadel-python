from rest_framework import serializers
import sys
sys.path.append("....")
from core.models import Request
sys.path.clear()
class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = [ 'id','address', 'created_at', 'area','cost_total','status','user','service']

    status = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    service = serializers.SerializerMethodField()

    def get_status(self, requests):
        return requests.status.status

    def get_user(self, requests):
        return requests.user.fullname

    def get_service(self, requests):
        return requests.service.name


