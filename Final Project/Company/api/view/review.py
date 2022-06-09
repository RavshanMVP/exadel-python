from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from api.serializers import ReviewSerializer
from core.models import Review, User, Request, Service
from core.utility import ReviewFilter


class ReviewDetails(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.select_related('request', 'service', 'user').order_by("created_at", "-rating")
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter

    def filter_queryset(self, queryset):
        filter_backends = (DjangoFilterBackend,)
        for backend in list(filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, view=self)
        return queryset

    def retrieve(self, request, pk=None):
        review = get_object_or_404(self.queryset, pk=pk)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        review = get_object_or_404(self.queryset, pk=pk)
        data = request.data
        service = Service.objects.get(name=data['service'])

        old_rating = float(service.company.company_rating) * int(service.company.ratings_count)
        deleted_rating = review.rating
        service.company.ratings_count -= 1
        new_rating = (old_rating - deleted_rating) / int(service.company.ratings_count)
        service.company.company_rating = new_rating
        service.company.save()

        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        data = request.data
        old_review = get_object_or_404(self.queryset, pk=pk)
        new_review = get_object_or_404(self.queryset, pk=pk)
        new_review.rating = data['rating']
        new_review.feedback = data['feedback']
        new_review.save()

        service = Service.objects.get(name=data['service'])

        current_rating = float(service.company.company_rating)
        current_count = int(service.company.ratings_count)
        rating_without_current = (current_rating * current_count - float(old_review.rating))
        service.company.company_rating = (rating_without_current + int(new_review.rating)) / current_count
        service.company.save()

        serializer = ReviewSerializer(new_review)
        return Response(serializer.data)

    def list(self, request):
        serializer = ReviewSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        user = User.objects.get(fullname=data['user'])
        service = Service.objects.get(name=data['service'])
        request = Request.objects.get(id=data['request'])

        if int(data["rating"]) < 1 or int(data["rating"]) > 5:
            raise ValueError("Ratings must be in the range from 1 to 5")

        if service.company.ratings_count > 0:
            service.company.company_rating = (float(service.company.company_rating) * float(
                service.company.ratings_count) + float(data["rating"])) / float(service.company.ratings_count + 1)
        else:
            service.company.company_rating = data["rating"]
        service.company.ratings_count += 1

        service.company.save()
        model = Review(rating=data['rating'], feedback=data['feedback'],
                       user=user, service=service, request=request)

        model.save()
        serializer = ReviewSerializer(model)
        return Response(serializer.data)
