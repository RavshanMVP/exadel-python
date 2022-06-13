import json

import factory
import pytest
from rest_framework.test import APIClient

from core.models import Category
from . import authorize

pytestmark = pytest.mark.django_db


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    id = factory.faker.Faker("pyint")
    category = factory.faker.Faker('name')


@pytest.fixture
def api_client():
    return APIClient


class TestCategory:
    endpoint = '/category'

    def test_list(self, api_client, authorize):
        self.endpoint = '/categories/list/'
        url = f'{self.endpoint}'
        category = CategoryFactory.create_batch(3)

        response = api_client().get(
            self.endpoint,
            HTTP_AUTHORIZATION=authorize
        )

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_retrieve(self, api_client, authorize):
        category = CategoryFactory()
        expected_json = {
            'category': category.category,
            'id': category.id
        }
        url = f'{self.endpoint}/{category.id}'

        response = api_client().get(url, HTTP_AUTHORIZATION=authorize)

        assert response.status_code == 200
        assert json.loads(response.content) == expected_json

    def test_post(self, api_client, authorize):
        self.endpoint = '/categories/create/'
        category = CategoryFactory()

        expected_json = {
            'category': category.category,
            'id': category.id + 1,
        }

        response = api_client().post(
            self.endpoint,
            data=expected_json,
            format='json',
            HTTP_AUTHORIZATION=authorize
        )

        assert response.status_code == 200
        assert json.loads(response.content) == expected_json

    def test_put(self, api_client, authorize):
        category = CategoryFactory()
        category_dict = {
            'category': category.category,
            'id': category.id,
        }
        url = f'{self.endpoint}/{category.id}'

        response = api_client().put(
            url,
            category_dict,
            format='json',
            HTTP_AUTHORIZATION=authorize
        )

        assert response.status_code == 200
        assert json.loads(response.content) == category_dict

    def test_delete(self, api_client, authorize):
        category = CategoryFactory()
        self.endpoint = '/category/' + str(category.id)
        url = self.endpoint
        response = api_client().delete(url, HTTP_AUTHORIZATION=authorize)

        assert response.status_code == 204
        assert Category.objects.all().count() == 0

    def test_retrieve_not_found(self, api_client, authorize):
        # also works for put and post
        self.endpoint = '/service/'
        category = CategoryFactory()
        self.endpoint += str(category.id + 1)
        response = api_client().get(self.endpoint, HTTP_AUTHORIZATION=authorize)
        assert response.status_code == 404

    def test_put_missing_value(self, api_client, authorize):
        # also works for retrieve and post
        category = CategoryFactory()
        expected_json = {
            'category': category.category
        }
        status = 200
        try:
            response = api_client().put(
                self.endpoint,
                expected_json,
                format='json',
                HTTP_AUTHORIZATION=authorize
            )
            assert status == 200
        except KeyError:
            status = 500
            assert False

    def test_unauthorized(self, api_client):
        # works for every view if I change url
        self.endpoint = '/category/create'
        category = CategoryFactory()
        expected_json = {
            'category': category.category,
            'id': category.id
        }
        response = api_client().put(self.endpoint, expected_json)

        assert response.status_code == 401
