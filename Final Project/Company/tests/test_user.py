import factory
import pytest
from rest_framework.test import APIClient
from core.models import Role, User
from .test_role import RoleFactory
from api.view import UserDetails
from rest_framework.permissions import AllowAny, IsAuthenticated
import json


pytestmark = pytest.mark.django_db

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model =User
    id = factory.faker.Faker("pyint")
    fullname = factory.faker.Faker('name')
    email = factory.faker.Faker('email')
    role = factory.SubFactory(RoleFactory)
    password = factory.faker.Faker("name")



@pytest.fixture
def api_client():
    return APIClient


class TestUser:
    endpoint = '/user'

    def test_list(self, api_client):
        UserDetails.permission_classes = [AllowAny]
        self.endpoint = '/users/list/'
        url = f'{self.endpoint}'
        category = UserFactory.create_batch(3)


        response = api_client().get(
            self.endpoint
        )
        assert response.status_code == 200
        UserDetails.permission_classes = [IsAuthenticated]
        assert len(json.loads(response.content)) == 3


    def test_retrieve(self, api_client):
        UserDetails.permission_classes = [AllowAny]
        user = UserFactory()
        expected_json = {
            'fullname':user.fullname,
            'email':user.email,
            'phone_number' : user.phone_number,
            'role':user.role.role,
            'id':user.id,
            'password':user.password
        }
        url = f'{self.endpoint}/{user.id}'

        response = api_client().get(url)

        assert response.status_code == 200
        UserDetails.permission_classes = [IsAuthenticated]
        assert json.loads(response.content) == expected_json

    def test_post(self, api_client):


        UserDetails.permission_classes = [AllowAny]
        self.endpoint ='/users/create/'
        user = UserFactory()

        some_email = user.email + " "
        user.email = some_email
        expected_json = {
            'id':user.id+1,
            'fullname':user.fullname,
            'email': some_email,
            'phone_number' : user.phone_number,
            'role':user.role.role,
            'password':user.password
        }

        response = api_client().post(

            self.endpoint,
            data=expected_json,
            format='json'
        )
        assert response.status_code == 200
        assert json.loads(response.content) == expected_json
        UserDetails.permission_classes = [IsAuthenticated]

    def test_put(self, api_client):
        UserDetails.permission_classes = [AllowAny]
        user = UserFactory()
        user_dict = {
            'id':user.id,
            'fullname':user.fullname,
            'email':user.email,
            'phone_number' : user.phone_number,
            'role':user.role.role,
            'password':user.password
        }
        url = f'{self.endpoint}/{user.id}'

        response = api_client().put(
            url,
            user_dict,
            format='json'
        )

        assert response.status_code == 200
        assert json.loads(response.content) == user_dict
        UserDetails.permission_classes = [IsAuthenticated]

    def test_delete(self, api_client):
        UserDetails.permission_classes = [AllowAny]
        user = UserFactory()
        self.endpoint = '/user/'+ str(user.id)
        url = self.endpoint
        response = api_client().delete(url)

        assert response.status_code == 204
        assert User.objects.all().count() == 0
        UserDetails.permission_classes = [IsAuthenticated]
