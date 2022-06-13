from rest_framework import serializers
from core.models import Response


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ['id', 'request', 'is_accepted', 'service', 'is_completed']

    request = serializers.SerializerMethodField()
    service = serializers.SerializerMethodField()

    def get_request(self, responses):
        return responses.request.id

    def get_service(self, responses):
        return responses.service.name
