from rest_framework import serializers
from core.models import Response

class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = [ 'id','request', 'is_accepted']

    request = serializers.SerializerMethodField()

    def get_request(self, response):
        return response.request.id

