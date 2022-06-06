from rest_framework import serializers
from core.models import Response


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ['id', 'request', 'is_accepted', 'service']

    request = serializers.SerializerMethodField()
    service = serializers.SerializerMethodField()

    def get_request(self, response):
        return response.request.id

    def get_service(self, response):
        return response.service.name
