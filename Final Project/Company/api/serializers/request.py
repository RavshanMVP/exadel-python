from rest_framework import serializers
from core.models import Request
from .service import ServiceSerializer


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['id', 'address', 'created_at', 'area', 'cost_total', 'status', 'user', 'final_service', 'country',
                  'city', 'minutes', 'service_list', 'accepted_list',
                  'is_filtered', 'min_rating', 'max_cost', 'search_category']

    status = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    final_service = serializers.SerializerMethodField()
    service_list = ServiceSerializer(read_only=False, many=True)
    accepted_list = ServiceSerializer(read_only=False, many=True)

    def get_status(self, requests):
        if requests.status is not None:
            return requests.status.status

    def get_user(self, requests):
        return requests.user.fullname

    def get_final_service(self, requests):
        if requests.final_service is not None:
            return requests.final_service.name

    def get_service_list(self, requests):
        if requests.service_list is not None:
            return requests.service_list.name

    def get_accepted_list(self, requests):
        if requests.accepted_list is not None:
            return requests.service_list.name
