from rest_framework.response import Response
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny

from api.serializers import ReviewSerializer
from core.models import Review, User, Request, Service

class ReviewDetails(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def retrieve(self, request, pk=None):
        queryset = Review.objects.all()
        review = get_object_or_404(queryset, pk=pk)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)


    def delete(self,request,pk,format = None):
        queryset = Review.objects.all()
        review = get_object_or_404(queryset, pk=pk)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self,request,pk,format = None):
        data = request.data
        review_list = Review.objects.all()
        review = get_object_or_404(review_list, pk=pk)
        review.rating = data['rating']
        review.created_at = data['created_at']
        review.feedback = data['feedback']
        review.user = User.objects.get(id=data['user'])
        review.service = Service.objects.get(id=data['service'])
        review.request = Request.objects.get(id=data['request'])
        review.save()

        serializer = ReviewSerializer(review)
        return Response(serializer.data)


    def list(self, request):
        queryset = Review.objects.all()
        serializer = ReviewSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self,request):
        data = request.data
        user = User.objects.get(id=data['user'])
        service = Service.objects.get(id=data['service'])
        request = Request.objects.get(id=data['request'])
        model = Review(rating = data['rating'], feedback = data['feedback'], created_at = data ['created_at'], user = user,service = service, request = request)
        model.save()
        serializer = ReviewSerializer(model)
        return Response(serializer.data)
