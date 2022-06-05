from rest_framework.response import Response
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import HttpResponse
from api.serializers import ReviewSerializer
from core.models import Review, User, Request, Service

class ReviewDetails(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.select_related('request','service','user').order_by("created_at","-rating")
    serializer_class = ReviewSerializer

    def retrieve(self, request, pk=None):
        review = get_object_or_404(self.queryset, pk=pk)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)


    def delete(self,request,pk,format = None):
        review = get_object_or_404(self.queryset, pk=pk)
        data = request.data
        user = User.objects.get(fullname = data["user"])

        old_rating = float(user.company_rating)*int(user.ratings_count)
        deleted_rating = review.rating
        user.ratings_count -=1
        new_rating = (old_rating - deleted_rating) / int(user.ratings_count)
        user.company_rating = new_rating
        user.save()

        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self,request,pk,format = None):
        data = request.data
        old_review = get_object_or_404(self.queryset, pk = pk)
        new_review = get_object_or_404(self.queryset, pk=pk)
        new_review.rating = data['rating']
        new_review.feedback = data['feedback']
        new_review.save()

        user = User.objects.get(fullname=data['user'])

        current_rating = float(user.company_rating)
        current_count = int(user.ratings_count)
        rating_without_current = (current_rating * current_count - float(old_review.rating))
        user.company_rating = (rating_without_current+ int(new_review.rating))/current_count
        user.save()

        serializer = ReviewSerializer(new_review)
        return Response(serializer.data)


    def list(self, request):
        serializer = ReviewSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def post(self,request):
        data = request.data
        user = User.objects.get(fullname=data['user'])
        service = Service.objects.get(name=data['service'])
        request = Request.objects.get(id=data['request'])


        user.company_rating = (float(user.company_rating) * float(user.ratings_count)
                               + float(data["rating"]))/float(user.ratings_count+1)

        user.ratings_count+=1
        user.save()
        model = Review(rating = data['rating'], feedback = data['feedback'], created_at = data ['created_at'],
                        user = user,service = service, request = request)

        model.save()
        serializer = ReviewSerializer(model)
        return Response(serializer.data)
