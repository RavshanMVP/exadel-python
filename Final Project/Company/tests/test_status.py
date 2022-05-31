import factory
import faker
import pytest
from rest_framework.test import APIClient
from core.models import RequestStatus
import json

pytestmark = pytest.mark.django_db

class RequestStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RequestStatus
    status = factory.faker.Faker('job')
    id = factory.faker.Faker("pyint")



@pytest.fixture
def api_client():
    return APIClient


class TestStatus:
    endpoint = '/statuses/'
    def test_list(self, api_client):
        self.endpoint = '/roles/list/'
        url = f'{self.endpoint}'
        status = RequestStatusFactory.create_batch(3)


        response = api_client().get(
            self.endpoint
        )

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_retrieve(self, api_client):
        request = RequestStatusFactory()
        expected_json = {
            'status': request.status,
            'id':request.id
        }
        url = f'{self.endpoint[:-3]}/{request.id}'

        response = api_client().get(url)

        assert response.status_code == 200
        assert json.loads(response.content) == expected_json

    def test_list_not_found(self, api_client):
        self.endpoint = '/categories/listt/'
        service= RequestStatusFactory.create_batch(3)
        response = api_client().get( self.endpoint)
        assert response.status_code == 404





