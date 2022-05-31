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
    CategoryDetails.permission_classes = [AllowAny]
    def test_list(self, api_client):
        self.endpoint = '/categories/list/'
        url = f'{self.endpoint}'
        category = CategoryFactory.create_batch(3)

        response = api_client().get(
            self.endpoint
        )

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

        assert response.status_code == 200
        assert json.loads(response.content) ==category_dict


    def test_delete(self, api_client):
        category = CategoryFactory()
        self.endpoint = '/category/'+ str(category.id)
        url = self.endpoint
        response = api_client().delete(url)

        assert response.status_code == 204
        assert Category.objects.all().count() == 0


    def test_list_not_found(self, api_client):
        self.endpoint = '/category/list/'
        category= CategoryFactory.create_batch(3)
        response = api_client().get( self.endpoint)
        assert response.status_code == 404

    def test_retrieve_not_found(self, api_client):
        #also works for put and post
        self.endpoint = '/service/'
        category= CategoryFactory()
        self.endpoint +=str(category.id+1)
        response = api_client().get( self.endpoint)
        assert response.status_code == 404

    def test_create_not_found(self, api_client):
        self.endpoint = '/service/create/1'
        category = CategoryFactory.create_batch(1)
        response = api_client().get( self.endpoint)
        assert response.status_code == 404

    def test_put_missing_value(self,api_client):
        #also works for retrieve and post
        category = CategoryFactory()
        expected_json = {
            'category': category.category
        }
        assert len(expected_json) < 2

    def test_unauthorized(self, api_client):
        #works for every view if I change url
        CategoryDetails.permission_classes = [IsAuthenticated]
        self.endpoint ='/category/'
        category = CategoryFactory()
        expected_json = {
            'category': category.category,
            'id':category.id
        }
        self.endpoint+=str(category.id)
        response = api_client().get(self.endpoint)

        assert response.status_code == 401
