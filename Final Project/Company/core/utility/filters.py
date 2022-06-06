from django_filters import rest_framework as filter
from core.models import Request, RequestStatus, Role, Response, Review, User, Service, Category


class UserFilter(filter.FilterSet):
    fullname = filter.CharFilter()
    company_rating = filter.RangeFilter()

    class Meta:
        model = User
        fields = ['fullname', 'company_rating']


class ServiceFilter(filter.FilterSet):
    name = filter.CharFilter()
    company = filter.RangeFilter(field_name="company__company_rating")
    cost = filter.RangeFilter()
    category = filter.CharFilter(field_name="category__category")

    class Meta:
        model = Service
        fields = ['name', 'company', 'cost', 'category']


class RequestFilter(filter.FilterSet):
    cost_total = filter.RangeFilter(field_name="service__cost")
    rating = filter.RangeFilter(field_name="service__company__company_rating")

    class Meta:
        model = Request
        fields = ['address']


class ReviewFilter(filter.FilterSet):
    created_at = filter.DateTimeFilter()

    class Meta:
        model = Review
        fields = ['created_at']
