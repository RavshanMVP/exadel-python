from rest_framework import serializers
from core.models import Service, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [ 'id', 'category']

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [ 'id', 'name', 'cost','company','category']

    company = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    def get_company(self,service):
        return service.company.fullname

    def get_category(self,service):
        return service.category.category

