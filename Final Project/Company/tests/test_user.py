import factory
import pytest
from rest_framework.test import APIClient
from core.models import Role, User
from .test_role import RoleFactory
from api.view import UserDetails
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
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

@pytest.fixture
def authorize():
    role = Role.objects.create(role='User')
    user = User.objects.create_user(fullname="Random name", email='random@gmail.com', password='12qwerty34',
                                    phone_number="+99893123", role = role)
    create_user = APIClient().post("/auth/jwt/create/", {"email": 'random@gmail.com', "password": "12qwerty34"})
    token_dict = json.loads(create_user.content.decode('utf-8'))
    token = token_dict["access"]
    return "Bearer " + token


class TestUser:
    endpoint = '/user'
    def test_list(self, api_client):
        self.endpoint = '/users/list/'
        url = f'{self.endpoint}'
        category = UserFactory.create_batch(3)

        response = api_client().get(
            self.endpoint
        )
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3


    def test_retrieve(self, api_client):
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
        assert json.loads(response.content) == expected_json

    def test_post(self, api_client, authorize):
        self.endpoint ='/users/create/'
        user = UserFactory()
        some_email = user.email +"1"
        expected_json = {
            'id':user.id+1,
            'fullname':user.fullname,
            'email': some_email,
            'phone_number' : user.phone_number,
            'role':user.role.role,
            'password':user.password
        }
        user.email +="1"
        response = api_client().post(
            self.endpoint,
            data=expected_json,
            format='json',
            HTTP_AUTHORIZATION =authorize,
        )
        assert response.status_code == 200
        assert json.loads(response.content) == expected_json

    def test_put(self, api_client, authorize):
        user = UserFactory()
        user_dict = {
            'id':user.id,
            'fullname':user.fullname,
            'email':user.email,
            'phone_number' : user.phone_number,
            'role':user.role.role,
            'password':user.password,
        }
        url = f'{self.endpoint}/{user.id}'

        response = api_client().put(
            url,
            user_dict,
            format='json',
            HTTP_AUTHORIZATION = authorize,
        )
        assert response.status_code == 200
        assert json.loads(response.content) == user_dict

    def test_delete(self, api_client, authorize):
        user = UserFactory()
        self.endpoint = '/user/'+ str(user.id)
        url = self.endpoint
        response = api_client().delete(url, HTTP_AUTHORIZATION = authorize,)

        assert response.status_code == 204
        assert User.objects.all().count() == 1


    def test_retrieve_not_found(self, api_client):
        #also works for put and post
        self.endpoint = '/user/'
        user = UserFactory()
        self.endpoint +=str(user.id+1)
        response = api_client().get( self.endpoint)
        assert response.status_code == 404


    def test_put_missing_value(self,api_client, authorize):
        #also works for retrieve and post
        user = UserFactory()
        user_dict = {
            'id':user.id,
            'fullname':user.fullname,
            'email':user.email,
            'role':user.role.role,
            'password':user.password,
        }
        url = f'{self.endpoint}/{user.id}'
        status = 200
        try:
            response = api_client().put(
                url,
                user_dict,
                format='json',
                HTTP_AUTHORIZATION = authorize
            )
            assert False
        except KeyError:
            assert True


    def test_ReadOnly_post(self, api_client):
        #also works for put
        self.endpoint ='/users/create/'
        user = UserFactory()
        expected_json = {
            'id':user.id+1,
            'fullname':user.fullname,
            'email':user.email,
            'phone_number' : user.phone_number,
            'role':user.role.role,
            'password':user.password,
        }
        response = api_client().post(self.endpoint, expected_json)

        assert response.status_code == 401

    def test_ReadOnly_get(self,api_client):
        self.endpoint = '/user/'
        user = UserFactory()
        self.endpoint +=str(user.id)
        response = api_client().get( self.endpoint)
        assert response.status_code == 200

    def test_ReadOnly_delete(self,api_client):
        self.endpoint = '/user/'
        user = UserFactory()
        self.endpoint +=str(user.id)
        response = api_client().delete( self.endpoint)
        assert response.status_code == 401
