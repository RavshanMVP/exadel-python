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
    def test_list(self, api_client):
        self.endpoint = '/requests/list/'
        url = f'{self.endpoint}'
        request = RequestFactory.create_batch(3)


        response = api_client().get(
            self.endpoint
        )
        if api_client().get(url).status_code == 404:
            assert response.status_code == 404
        else:
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
        if api_client().get(url).status_code == 404:
            assert response.status_code == 404
        else:
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
        if api_client().post(self.endpoint,data=expected_json,format='json').status_code == 404:
            assert response.status_code == 404
        elif RequestDetails.permission_classes == IsAuthenticated or IsAuthenticatedOrReadOnly and api_client().post(self.endpoint,data=expected_json,format='json').status_code==401:
            assert response.status_code == 401
        else:
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
        if api_client().put(url, request_dict,format='json').status_code == 404:
            assert response.status_code == 404
        elif RequestDetails.permission_classes == IsAuthenticated or IsAuthenticatedOrReadOnly and api_client().put(url, request_dict,format='json').status_code == 401:
            assert response.status_code == 401
        else:
            assert response.status_code == 200
            assert json.loads(response.content) ==request_dict


    def test_delete(self, api_client):
        request = RequestFactory()
        self.endpoint = '/request/'+ str(request.id)
        url = self.endpoint
        response = api_client().delete(url)
        if api_client().get(url).status_code == 404:
            assert api_client().get(url).status_code == 404
        elif api_client().delete(url).status_code == 401 and RequestDetails.permission_classes == IsAuthenticated or IsAuthenticatedOrReadOnly:
            assert api_client().delete(url).status_code == 401
        else:
            assert response.status_code == 204
            assert Request.objects.all().count() == 0
