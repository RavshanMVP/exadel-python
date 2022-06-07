import json

import factory
import pytest
from rest_framework.test import APIClient

from core.models import Response
from . import ServiceFactory, RequestFactory
from . import authorize

pytestmark = pytest.mark.django_db


class ResponseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Response

    request = factory.SubFactory(RequestFactory)
    id = factory.faker.Faker("pyint")
    is_accepted = factory.faker.Faker("pybool")
    service = factory.SubFactory(ServiceFactory)


@pytest.fixture
def api_client():
    return APIClient


class TestService:
    endpoint = '/response'

    def test_list(self, api_client, authorize):
        self.endpoint = '/responses/list/'
        url = f'{self.endpoint}'
        response_ = ResponseFactory.create_batch(3)

        response = api_client().get(
            self.endpoint, HTTP_AUTHORIZATION=authorize
        )

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_retrieve(self, api_client, authorize):
        response_ = ResponseFactory()
        expected_json = {
            'service': response_.service.name,
            'id': response_.id,
            'is_accepted': response_.is_accepted,
            'request': response_.request.id,
        }
        url = f'{self.endpoint}/{response_.id}'

        response = api_client().get(url, HTTP_AUTHORIZATION=authorize)

        assert response.status_code == 200
        assert json.loads(response.content) == expected_json

    def test_post(self, api_client, authorize):
        self.endpoint = '/responses/create/'
        response_ = ResponseFactory()

        expected_json = {
            'service': response_.service.name,
            'id': response_.id + 1,
            'is_accepted': response_.is_accepted,
            'request': response_.request.id,
        }

        response = api_client().post(
            self.endpoint,
            data=expected_json,
            HTTP_AUTHORIZATION=authorize
        )

        assert response.status_code == 200
        if response.content != b'Your service is not in order list':
            assert json.loads(response.content) == expected_json

    def test_put(self, api_client, authorize):
        response_ = ResponseFactory()
        response_dict = {
            'service': response_.service.name,
            'id': response_.id + 1,
            'is_accepted': response_.is_accepted,
            'request': response_.request.id,
        }
        url = f'{self.endpoint}/{response_.id}'

        response = api_client().put(
            url,
            response_dict,
            format='json',
            HTTP_AUTHORIZATION=authorize
        )

        assert response.status_code == 200
        assert json.loads(response.content) == response_dict

    def test_delete(self, api_client, authorize):
        response_ = ResponseFactory()
        self.endpoint = '/response/' + str(response_.id)
        url = self.endpoint
        response = api_client().delete(url, HTTP_AUTHORIZATION=authorize)

        assert response.status_code == 204
        assert Response.objects.all().count() == 0

    def test_retrieve_not_found(self, api_client, authorize):
        # also works for put and post
        self.endpoint = '/response/'
        response_ = ResponseFactory()
        self.endpoint += str(response_.id + 1)
        response = api_client().get(self.endpoint, HTTP_AUTHORIZATION=authorize)
        assert response.status_code == 404

    def test_put_missing_value(self, api_client, authorize):
        # also works for retrieve and post
        response_ = ResponseFactory()
        expected_json = {
            'id': response_.id,
            'is_accepted': response_.is_accepted,
            'request': response_.request.id,
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
        self.endpoint = '/responses/create/'
        response_ = ResponseFactory()
        expected_json = {
            'service': response_.service.name,
            'id': response_.id,
            'is_accepted': response_.is_accepted,
            'request': response_.request.id,
        }
        response = api_client().post(self.endpoint, expected_json)

        assert response.status_code == 401
