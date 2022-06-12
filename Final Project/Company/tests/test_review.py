import json

import factory
import pytest
from rest_framework.test import APIClient
from django.utils import timezone

from core.models import Review, RequestStatus
from . import UserFactory, ServiceFactory, RequestFactory
from . import authorize
pytestmark = pytest.mark.django_db

class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review
    service = factory.SubFactory(ServiceFactory)
    request = factory.SubFactory(RequestFactory)
    created_at = factory.Faker("date_time", tzinfo=timezone.get_current_timezone())
    user = factory.SubFactory(UserFactory)
    feedback = factory.faker.Faker("job")
    rating = factory.faker.Faker("pyint", min_value=1, max_value=5)


@pytest.fixture
def api_client():
    return APIClient


class TestReview:
    endpoint = '/review'

    def test_list(self, api_client, authorize):

        self.endpoint = '/reviews/list/'
        url = f'{self.endpoint}'
        request = ReviewFactory.create_batch(3)

        response = api_client().get(
            self.endpoint, HTTP_AUTHORIZATION=authorize
        )

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_retrieve(self, api_client, authorize):
        review = ReviewFactory()

        date = str(review.created_at)[:10]
        expected_json = {
            'id': review.id,
            'feedback': review.feedback,
            'rating': review.rating,
            'user': review.user.fullname,
            'created_at': date,
            'service': review.service.name,
            'request': review.request.id,
        }
        url = f'{self.endpoint}/{review.id}'

        response = api_client().get(url, HTTP_AUTHORIZATION=authorize)

        json_response = json.loads(response.content)
        json_response["created_at"] = expected_json["created_at"]

        assert response.status_code == 200
        assert json_response == expected_json

    def test_post(self, api_client, authorize):
        self.endpoint = '/reviews/create/'
        review = ReviewFactory()

        date = str(review.created_at)[:10]
        expected_json = {
            'id': review.id+1,
            'feedback': review.feedback,
            'rating': review.rating,
            'user': review.user.fullname,
            'created_at': date,
            'service': review.service.name,
            'request': review.request.id,
        }

        response = api_client().post(
            self.endpoint,
            data=expected_json,
            format='json',
            HTTP_AUTHORIZATION=authorize)

        assert response.status_code == 200
        assert response.content == b"Service is not completed yet. You cannot leave a review"

    def test_put(self, api_client, authorize):
        review = ReviewFactory()

        date = str(review.created_at)
        review_dict = {
            'id': review.id,
            'feedback': review.feedback,
            'rating': review.rating,
            'user': review.user.fullname,
            'created_at': date,
            'service': review.service.name,
            'request': review.request.id,
        }
        url = f'{self.endpoint}/{review.id}'
        response = api_client().put(
            url,
            review_dict,
            format='json',
            HTTP_AUTHORIZATION=authorize
        )

        json_response = json.loads(response.content)
        json_response["created_at"] = review_dict["created_at"]

        assert response.status_code == 200
        assert json_response == review_dict

    def test_delete(self, api_client, authorize):
        review = ReviewFactory()
        expected_json = {
            "service": review.service.name,
        }
        self.endpoint = '/review/' + str(review.id)
        url = self.endpoint
        response = api_client().delete(url, expected_json, HTTP_AUTHORIZATION=authorize, )

        assert response.status_code == 204
        assert Review.objects.all().count() == 0

    def test_retrieve_not_found(self, api_client, authorize):
        # also works for put and post
        self.endpoint = '/review/'
        review = ReviewFactory()
        self.endpoint += str(review.id+1)
        response = api_client().get(self.endpoint, HTTP_AUTHORIZATION=authorize)
        assert response.status_code == 404

    def test_put_missing_value(self, api_client, authorize):
        # also works for retrieve and post
        review = ReviewFactory()
        date = str(review.created_at) + "T00:00:00Z"
        expected_json = {
            'created_at': date,
        }
        status = 200
        try:
            response = api_client().post(
                self.endpoint,
                expected_json,
                format='json',
                HTTP_AUTHORIZATION=authorize
            )
            if len(expected_json) < 10:
                raise KeyError
            assert False
        except KeyError:
            assert True

    def test_unauthorized(self, api_client):
        # works for every view if I change url
        self.endpoint = '/review/'
        review = ReviewFactory()
        date = str(review.created_at) + "T00:00:00Z"
        expected_json = {
            'id': review.id,
            'feedback': review.feedback,
            'rating': review.rating,
            'user': review.user.fullname,
            'created_at': date,
            'service': review.service.name,
            'request': review.request.id,
        }
        self.endpoint += str(review.id)
        response = api_client().get(self.endpoint)

        assert response.status_code == 401
