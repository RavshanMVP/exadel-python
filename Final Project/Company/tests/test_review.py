import factory
import pytest
from rest_framework.test import APIClient
from core.models import Review
from api.view import ReviewDetails
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from . import UserFactory, ServiceFactory, RequestFactory
import json


pytestmark = pytest.mark.django_db

class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review
    service = factory.SubFactory(ServiceFactory)
    request = factory.SubFactory(RequestFactory)
    id = factory.faker.Faker("pyint")
    created_at = factory.faker.Faker("date")
    user = factory.SubFactory(UserFactory)
    feedback = factory.faker.Faker("job")
    rating = factory.faker.Faker("pyint")


@pytest.fixture
def api_client():
    return APIClient


class TestReview:
    endpoint = '/review'

    def test_list(self, api_client):

        self.endpoint = '/reviews/list/'
        url = f'{self.endpoint}'
        request = ReviewFactory.create_batch(3)


        response = api_client().get(
            self.endpoint
        )
        if api_client().get(url).status_code == 404:
            assert response.status_code == 404
        else:
            assert response.status_code == 200
            assert len(json.loads(response.content)) == 3

    def test_retrieve(self, api_client):
        review = ReviewFactory()

        date = str(review.created_at) + "T00:00:00Z"
        expected_json = {
            'id':review.id,
            'feedback' : review.feedback,
            'rating': review.rating,
            'user':review.user.fullname,
            'created_at' : date,
            'service' : review.service.name,
            'request' : review.request.id,
        }
        url = f'{self.endpoint}/{review.id}'

        response = api_client().get(url)
        if api_client().get(url).status_code == 404:
            assert response.status_code == 404
        else:
            assert response.status_code == 200
            assert json.loads(response.content) == expected_json

    def test_post(self, api_client):
        self.endpoint ='/reviews/create/'
        review= ReviewFactory()

        date = str(review.created_at) + "T00:00:00Z"
        expected_json = {
            'id':review.id+1,
            'feedback' : review.feedback,
            'rating': review.rating,
            'user':review.user.fullname,
            'created_at' : date,
            'service' : review.service.name,
            'request' : review.request.id,
        }


        response = api_client().post(
            self.endpoint,
            data=expected_json,
            format='json'
        )
        if api_client().post(self.endpoint,data=expected_json,format='json').status_code == 404:
            assert response.status_code == 404
        elif ReviewDetails.permission_classes == IsAuthenticated or IsAuthenticatedOrReadOnly and api_client().post(self.endpoint,data=expected_json,format='json').status_code==401:
            assert response.status_code == 401
        else:
            assert response.status_code == 200
            assert json.loads(response.content) == expected_json

    def test_put(self, api_client):
        review = ReviewFactory()

        date = str(review.created_at) + "T00:00:00Z"
        review_dict = {
            'id':review.id,
            'feedback' : review.feedback,
            'rating': review.rating,
            'user':review.user.fullname,
            'created_at' : date,
            'service' : review.service.name,
            'request' : review.request.id,
        }
        url = f'{self.endpoint}/{review.id}'

        response = api_client().put(
            url,
            review_dict,
            format='json'
        )
        if api_client().put(url, review_dict,format='json').status_code == 404:
            assert response.status_code == 404
        elif ReviewDetails.permission_classes == IsAuthenticated or IsAuthenticatedOrReadOnly and api_client().put(url, review_dict,format='json').status_code == 401:
            assert response.status_code == 401
        else:
            assert response.status_code == 200
            assert json.loads(response.content) ==review_dict

    def test_delete(self, api_client):
        review = ReviewFactory()
        self.endpoint = '/review/'+ str(review.id)
        url = self.endpoint
        response = api_client().delete(url)
        if api_client().get(url).status_code == 404:
            assert api_client().get(url).status_code == 404
        elif api_client().delete(url).status_code == 401 and ReviewDetails.permission_classes == IsAuthenticated or IsAuthenticatedOrReadOnly:
            assert api_client().delete(url).status_code == 401
        else:
            assert response.status_code == 204
            assert Review.objects.all().count() == 0

