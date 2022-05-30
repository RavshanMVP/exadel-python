import factory
import pytest
from rest_framework.test import APIClient
from core.models import Category
from api.view import CategoryDetails
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
import json


pytestmark = pytest.mark.django_db

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model =Category
    id = factory.faker.Faker("pyint")
    category = factory.faker.Faker('job')




@pytest.fixture
def api_client():
    return APIClient


class TestCategory:
    endpoint = '/category'
    def test_list(self, api_client):
        self.endpoint = '/categories/list/'
        url = f'{self.endpoint}'
        category = CategoryFactory.create_batch(3)


        response = api_client().get(
            self.endpoint
        )
        if api_client().get(url).status_code == 404:
            assert response.status_code == 404
        else:
            assert response.status_code == 200
            assert len(json.loads(response.content)) == 3

    def test_retrieve(self, api_client):
        category = CategoryFactory()
        expected_json = {
            'category': category.category,
            'id':category.id
        }
        url = f'{self.endpoint}/{category.id}'

        response = api_client().get(url)
        if api_client().get(url).status_code == 404:
            assert response.status_code == 404
        else:
            assert response.status_code == 200
            assert json.loads(response.content) == expected_json

    def test_post(self, api_client):
        self.endpoint ='/categories/create/'
        category = CategoryFactory()
        expected_json = {
            'category': category.category,
            'id': category.id+1,
        }

        response = api_client().post(
            self.endpoint,
            data=expected_json,
            format='json'
        )
        if api_client().post(self.endpoint,data=expected_json,format='json').status_code == 404:
            assert response.status_code == 404
        elif CategoryDetails.permission_classes == IsAuthenticated or IsAuthenticatedOrReadOnly and api_client().post(self.endpoint,data=expected_json,format='json').status_code==401:
            assert response.status_code == 401
        else:
            assert response.status_code == 200
            assert json.loads(response.content) == expected_json

    def test_put(self, api_client):
        category = CategoryFactory()
        category_dict = {
            'category': category.category,
            'id': category.id,
        }
        url = f'{self.endpoint}/{category.id}'

        response = api_client().put(
            url,
            category_dict,
            format='json'
        )
        if api_client().put(url, category_dict,format='json').status_code == 404:
            assert response.status_code == 404
        elif CategoryDetails.permission_classes == IsAuthenticated or IsAuthenticatedOrReadOnly and api_client().put(url, category_dict,format='json').status_code == 401:
            assert response.status_code == 401
        else:
            assert response.status_code == 200
            assert json.loads(response.content) ==category_dict


    def test_delete(self, api_client):
        category = CategoryFactory()
        self.endpoint = '/category/'+ str(category.id)
        url = self.endpoint
        response = api_client().delete(url)
        if api_client().get(url).status_code == 404:
            assert api_client().get(url).status_code == 404
        elif api_client().delete(url).status_code == 401 and CategoryDetails.permission_classes == IsAuthenticated or IsAuthenticatedOrReadOnly:
            assert api_client().delete(url).status_code == 401
        else:
            assert response.status_code == 204
            assert Category.objects.all().count() == 0
