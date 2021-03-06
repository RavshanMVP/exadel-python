import factory
import pytest
from rest_framework.test import APIClient
from core.models import Role
import json

pytestmark = pytest.mark.django_db


class RoleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Role
    role = factory.Iterator(["user", "Comp"])
    id = factory.faker.Faker("pyint")


@pytest.fixture
def api_client():
    return APIClient


class TestRole:
    endpoint = '/roles/'

    def test_list(self, api_client):
        self.endpoint = '/roles/list/'
        role = RoleFactory.create_batch(3)

        response = api_client().get(
            self.endpoint
        )

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_retrieve(self, api_client):
        role = RoleFactory()
        expected_json = {
            'role': role.role,
            'id': role.id
        }
        url = f'{self.endpoint[:-2]}/{role.id}'

        response = api_client().get(url)

        assert response.status_code == 200
        assert json.loads(response.content) == expected_json

    def test_list_not_found(self, api_client):
        self.endpoint = '/rolles/list/'
        service = RoleFactory.create_batch(3)
        response = api_client().get(self.endpoint)
        assert response.status_code == 404
