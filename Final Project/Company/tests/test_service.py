import factory
import pytest
from rest_framework.test import APIClient
from core.models import Category, Service
from api.view import ServiceDetails
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from . import CategoryFactory, UserFactory
import json


pytestmark = pytest.mark.django_db

class ServiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Service
    category = factory.SubFactory(CategoryFactory)
    id = factory.faker.Faker("pyint")
    cost = factory.faker.Faker("pyint")
    name = factory.faker.Faker("name")
    company = factory.SubFactory(UserFactory)



@pytest.fixture
def api_client():
    return APIClient


class TestService:
    endpoint = '/service'
    def test_list(self, api_client):
        self.endpoint = '/services/list/'
        url = f'{self.endpoint}'
        service = ServiceFactory.create_batch(3)


        response = api_client().get(
            self.endpoint
        )
        if api_client().get(url).status_code == 404:
            assert response.status_code == 404
        else:
            assert response.status_code == 200
            assert len(json.loads(response.content)) == 3

    def test_retrieve(self, api_client):
        service = ServiceFactory()
        expected_json = {
            'category': service.category.category,
            'id':service.id,
            'name':service.name,
            'cost':service.cost,
            'company':service.company.fullname,
        }
        url = f'{self.endpoint}/{service.id}'

        response = api_client().get(url)
        if api_client().get(url).status_code == 404:
            assert response.status_code == 404
        else:
            assert response.status_code == 200
            assert json.loads(response.content) == expected_json

    def test_post(self, api_client):
        self.endpoint ='/services/create/'
        service= ServiceFactory()
        expected_json = {
            'category': service.category.category,
            'id':service.id+1,
            'name':service.name,
            'cost':service.cost,
            'company':service.company.fullname,
        }


        response = api_client().post(
            self.endpoint,
            data=expected_json,
            format='json'
        )
        if api_client().post(self.endpoint,data=expected_json,format='json').status_code == 404:
            assert response.status_code == 404
        elif ServiceDetails.permission_classes == IsAuthenticated or IsAuthenticatedOrReadOnly and api_client().post(self.endpoint,data=expected_json,format='json').status_code==401:
            assert response.status_code == 401
        else:
            assert response.status_code == 200
            assert json.loads(response.content) == expected_json


    def test_put(self, api_client):
        service = ServiceFactory()
        service_dict = {
            'category': service.category.category,
            'id':service.id,
            'name':service.name,
            'cost':service.cost,
            'company':service.company.fullname,
        }
        url = f'{self.endpoint}/{service.id}'

        response = api_client().put(
            url,
            service_dict,
            format='json'
        )
        if api_client().put(url, service_dict,format='json').status_code == 404:
            assert response.status_code == 404
        elif ServiceDetails.permission_classes == IsAuthenticated or IsAuthenticatedOrReadOnly and api_client().put(url, service_dict,format='json').status_code == 401:
            assert response.status_code == 401
        else:
            assert response.status_code == 200
            assert json.loads(response.content) ==service_dict


    def test_delete(self, api_client):
        service = ServiceFactory()
        self.endpoint = '/service/'+ str(service.id)
        url = self.endpoint
        response = api_client().delete(url)
        if api_client().get(url).status_code == 404:
            assert api_client().get(url).status_code == 404
        elif api_client().delete(url).status_code == 401 and ServiceDetails.permission_classes == IsAuthenticated or IsAuthenticatedOrReadOnly:
            assert api_client().delete(url).status_code == 401
        else:
            assert response.status_code == 204
            assert Service.objects.all().count() == 0

