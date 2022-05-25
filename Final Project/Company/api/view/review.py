from rest_framework.response import Response
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny

from api.serializers import ReviewSerializer
from core.models import Review, User, Request, Service

class ReviewDetails(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Review.objects.select_related('request','service','user').order_by("created_at","-rating")
    serializer_class = ReviewSerializer

    def retrieve(self, request, pk=None):
        review = get_object_or_404(self.queryset, pk=pk)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)


    def delete(self,request,pk,format = None):
        review = get_object_or_404(self.queryset, pk=pk)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self,request,pk,format = None):
        data = request.data
        review = get_object_or_404(self.queryset, pk=pk)
        review.rating = data['rating']
        review.feedback = data['feedback']
        review.save()

        serializer = ReviewSerializer(review)
        return Response(serializer.data)


    def list(self, request):
        serializer = ReviewSerializer(self.queryset, many=True)
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
