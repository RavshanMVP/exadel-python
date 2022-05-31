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
    ReviewDetails.permission_classes = [AllowAny]
    def test_list(self, api_client):

        self.endpoint = '/reviews/list/'
        url = f'{self.endpoint}'
        request = ReviewFactory.create_batch(3)

        response = api_client().get(
            self.endpoint
        )

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

        assert response.status_code == 200
        assert json.loads(response.content) ==review_dict

    def test_delete(self, api_client):
        review = ReviewFactory()
        self.endpoint = '/review/'+ str(review.id)
        url = self.endpoint
        response = api_client().delete(url)

        assert response.status_code == 204
        assert Review.objects.all().count() == 0

    def test_list_not_found(self, api_client):
        self.endpoint = '/review/list/'
        review= ReviewFactory.create_batch(3)
        response = api_client().get( self.endpoint)
        assert response.status_code == 404

    def test_retrieve_not_found(self, api_client):
        #also works for put and post
        self.endpoint = '/review/'
        review= ReviewFactory()
        self.endpoint +=str(review.id+1)
        response = api_client().get( self.endpoint)
        assert response.status_code == 404

    def test_create_not_found(self, api_client):
        self.endpoint = '/review/create/1'
        review = ReviewFactory.create_batch(1)
        response = api_client().get( self.endpoint)
        assert response.status_code == 404

    def test_put_missing_value(self,api_client):
        #also works for retrieve and post
        review = ReviewFactory()
        date = str(review.created_at) + "T00:00:00Z"
        expected_json = {
            'id':review.id,
            'created_at' : date,
        }
        assert len(expected_json) < 7

    def test_unauthorized(self, api_client):
        #works for every view if I change url
        ReviewDetails.permission_classes = [IsAuthenticated]
        self.endpoint ='/review/'
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
        self.endpoint+=str(review.id)
        response = api_client().get(self.endpoint)

        assert response.status_code == 401
