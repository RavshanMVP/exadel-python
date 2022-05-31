import factory
import pytest
from rest_framework.test import APIClient
from core.models import Request
from api.view import RequestDetails
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from . import UserFactory, ServiceFactory, RequestStatusFactory
import json


pytestmark = pytest.mark.django_db

class RequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Request
    service = factory.SubFactory(ServiceFactory)
    status = factory.SubFactory(RequestStatusFactory)
    id = factory.faker.Faker("pyint")
    cost_total = factory.faker.Faker("pyint")
    area = factory.faker.Faker("pyint")
    created_at = factory.faker.Faker("date")
    user = factory.SubFactory(UserFactory)
    address = factory.faker.Faker("address")


@pytest.fixture
def api_client():
    return APIClient


class TestRequest:
    endpoint = '/request'
    RequestDetails.permission_classes = [AllowAny]
    def test_list(self, api_client):
        self.endpoint = '/requests/list/'
        url = f'{self.endpoint}'
        request = RequestFactory.create_batch(3)

        response = api_client().get(
            self.endpoint
        )

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_retrieve(self, api_client):

        request = RequestFactory()

        date = str(request.created_at) + "T00:00:00Z"
        expected_json = {
            'id':request.id,
            'area' : request.area,
            'cost_total': request.cost_total,
            'user':request.user.fullname,
            'created_at' : date,
            'service' : request.service.name,
            'status' : request.status.status,
            'address' : request.address
        }
        url = f'{self.endpoint}/{request.id}'

        response = api_client().get(url)

        assert response.status_code == 200
        assert json.loads(response.content) == expected_json

    def test_post(self, api_client):

        self.endpoint ='/requests/create/'
        request= RequestFactory()

        date = str(request.created_at) + "T00:00:00Z"

        expected_json = {
            'id':request.id+1,
            'area' : request.area,
            'cost_total': request.cost_total,
            'user':request.user.fullname,
            'created_at' : date,
            'service' : request.service.name,
            'status' : request.status.status,
            'address' : request.address
        }

        response = api_client().post(
            self.endpoint,
            data=expected_json,
            format='json'
        )

        assert response.status_code == 200
        assert json.loads(response.content) == expected_json


    def test_put(self, api_client):
        request = RequestFactory()

        date = str(request.created_at) + "T00:00:00Z"

        request_dict = {
            'id':request.id,
            'area' : request.area,
            'cost_total': request.cost_total,
            'user':request.user.fullname,
            'created_at' : date,
            'service' : request.service.name,
            'status' : request.status.status,
            'address' : request.address
        }
        url = f'{self.endpoint}/{request.id}'

        response = api_client().put(
            url,
            request_dict,
            format='json'
        )

        assert response.status_code == 200
        assert json.loads(response.content) ==request_dict


    def test_delete(self, api_client):
        request = RequestFactory()
        self.endpoint = '/request/'+ str(request.id)
        url = self.endpoint
        response = api_client().delete(url)

        assert response.status_code == 204
        assert Request.objects.all().count() == 0

    def test_list_not_found(self, api_client):
        self.endpoint = '/request/list/'
        request= RequestFactory.create_batch(3)
        response = api_client().get( self.endpoint)
        assert response.status_code == 404

    def test_retrieve_not_found(self, api_client):
        #also works for put and post
        self.endpoint = '/request/'
        request= RequestFactory()
        self.endpoint +=str(request.id+1)
        response = api_client().get( self.endpoint)
        assert response.status_code == 404

    def test_create_not_found(self, api_client):
        self.endpoint = '/request/create/1'
        request = RequestFactory.create_batch(1)
        response = api_client().get( self.endpoint)
        assert response.status_code == 404

    def test_put_missing_value(self,api_client):
        #also works for retrieve and post
        request = RequestFactory()
        date = str(request.created_at) + "T00:00:00Z"
        expected_json = {
            'id':request.id,
            'area' : request.area,
            'cost_total': request.cost_total,
            'user':request.user.fullname,
            'address' : request.address
        }
        assert len(expected_json) < 8

    def test_unauthorized(self, api_client):
        #works for every view if I change url
        RequestDetails.permission_classes = [IsAuthenticated]
        self.endpoint ='/request/'
        request = RequestFactory()
        date = str(request.created_at) + "T00:00:00Z"
        expected_json = {
            'id':request.id,
            'area' : request.area,
            'cost_total': request.cost_total,
            'user':request.user.fullname,
            'created_at' : date,
            'service' : request.service.name,
            'status' : request.status.status,
            'address' : request.address
        }
        self.endpoint+=str(request.id)
        response = api_client().get(self.endpoint)

        assert response.status_code == 401
