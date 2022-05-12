from rest_framework.response import Response
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import status

from api.serializers import ReviewSerializer
from core.models import Review

class ReviewDetails(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        queryset = Review.objects.all()
        review = get_object_or_404(queryset, pk=pk)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)


    def delete(self,request,pk,format = None):
        model = self.get_data(pk)
        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self,request,pk,format = None):
        model = self.get_data(pk)
        serializer = ReviewSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def list(self, request):
        queryset = Review.objects.all()
        serializer = ReviewSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self,request):
        data = request.data
        model = Review(fullname = data['fullname'], phone_number = data['phone_number'], email = data ['email'], role_id = data['role_id'])
        model.save()
        serializer = ReviewSerializer(model)
        return Response(serializer.data)
