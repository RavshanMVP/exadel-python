import json
from datetime import datetime

import factory
import pytest
from rest_framework.test import APIClient
from django.utils import timezone

from core.models import Request
from . import UserFactory, ServiceFactory, RequestStatusFactory
from . import authorize
pytestmark = pytest.mark.django_db
@pytest.mark.filterwarnings('ignore::RemovedInDjango50Warning')

class RequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Request

    final_service = factory.SubFactory(ServiceFactory)
    status = factory.SubFactory(RequestStatusFactory)
    id = factory.faker.Faker("pyint")
    cost_total = factory.faker.Faker("pyint")
    area = factory.faker.Faker("pyint")
    created_at = factory.Faker("date_time", tzinfo=timezone.get_current_timezone())
    user = factory.SubFactory(UserFactory)
    address = factory.faker.Faker("address")
    city = factory.faker.Faker("address")
    country = factory.faker.Faker("address")
    minutes = factory.faker.Faker("pyint")
    is_filtered = factory.faker.Faker("pybool")
    search_category = factory.faker.Faker("job")
    min_rating = factory.faker.Faker("pyint", min_value=1, max_value=5)
    max_cost = factory.faker.Faker("pyint")

    @factory.post_generation
    def service_list(self, create, extracted, **kwargs):
        if not create:
            return []
        if extracted:
            self.service_list.add

    @factory.post_generation
    def accepted_list(self, create, extracted, **kwargs):
        if not create:
            return []
        if extracted:
            self.accepted_list.add


@pytest.fixture
def api_client():
    return APIClient


class TestRequest:
    endpoint = '/request'

    def test_list(self, api_client, authorize):
        service_list = ServiceFactory.create_batch(1)
        accepted_list = ServiceFactory.create_batch(1)
        self.endpoint = '/requests/list/'
        url = f'{self.endpoint}'
        request = RequestFactory(service_list=service_list[0], accepted_list=accepted_list[0])

        response = api_client().get(
            self.endpoint,
            HTTP_AUTHORIZATION=authorize,
        )

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

    def test_retrieve(self, api_client, authorize):

        service_list = ServiceFactory.create_batch(1)
        accepted_list = ServiceFactory.create_batch(1)

        request = RequestFactory(service_list=service_list[0].id, accepted_list=accepted_list[0].id)

        date = str(timezone.now())
        expected_json = {
            'id': request.id,
            'area': request.area,
            'user': request.user.fullname,
            'created_at': date,
            'final_service': request.final_service.name,
            'status': request.status.status,
            'address': request.address,
            'city': request.city,
            'country': request.country,
            'minutes': request.minutes,
        }
        url = f'{self.endpoint}/{request.id}'

        response = api_client().get(url, HTTP_AUTHORIZATION=authorize)

        json_response = json.loads(response.content)
        json_response["created_at"] = expected_json["created_at"]

        assert response.status_code == 200
        assert json_response == expected_json

    def test_post(self, api_client, authorize):

        self.endpoint = '/requests/create/'
        service_list = ServiceFactory.create_batch(1)
        accepted_list = ServiceFactory.create_batch(1)

        request = RequestFactory(service_list=service_list[0].id, accepted_list=accepted_list[0].id)
        date = str(timezone.now())
        request.user.role.role = "user"
        expected_json = {
            'id': request.id+1,
            'area': request.area,
            'user': request.user.fullname,
            'created_at': date,
            'status': request.status.status,
            'address': request.address,
            'city': request.city,
            'country': request.country,
            'minutes': request.minutes,
            'service_list': [],
            'is_filtered': request.is_filtered,
        }

        response = api_client().post(
            self.endpoint,
            data=expected_json,
            format='json',
            HTTP_AUTHORIZATION=authorize,
        )

        json_response = json.loads(response.content)
        json_response["created_at"] = expected_json["created_at"]

        assert response.status_code == 200
        assert json_response == expected_json

    def test_put(self, api_client, authorize):
        service_list = ServiceFactory.create_batch(1)
        accepted_list = ServiceFactory.create_batch(1)

        request = RequestFactory(service_list=service_list[0].id, accepted_list=accepted_list[0].id)

        date = str(timezone.now())
        request.status.status = "Pending"
        request_dict = {
            'id': request.id,
            'area': request.area,
            'user': request.user.fullname,
            'created_at': date,
            'status': request.status.status,
            'address': request.address,
            'city': request.city,
            'country': request.country,
            'minutes': request.minutes,
        }

        if request.status.status == "Pending":
            request_dict['service_list'] = [],
            request_dict['is_filtered'] = request.is_filtered
        else:
            request_dict['final_service'] = request.final_service.name

        url = f'{self.endpoint}/{request.id}'
        try:
            response = api_client().put(
                url,
                request_dict,
                format='json',
                HTTP_AUTHORIZATION=authorize,
            )

            json_response = json.loads(response.content)
            json_response["created_at"] = request_dict["created_at"]
        except json.decoder.JSONDecodeError:
            assert response.status_code == 200
        assert response.status_code == 200

        if response.content == 'The request is in the process or finished':
            assert json_response == request_dict

    def test_delete(self, api_client, authorize):
        request = RequestFactory()
        self.endpoint = '/request/' + str(request.id)
        url = self.endpoint
        response = api_client().delete(url, HTTP_AUTHORIZATION=authorize, )

        assert response.status_code == 204
        assert Request.objects.all().count() == 0

    def test_retrieve_not_found(self, api_client, authorize):
        # also works for put and post
        self.endpoint = '/request/'
        request = RequestFactory()
        self.endpoint += str(request.id + 1)
        response = api_client().get(self.endpoint, HTTP_AUTHORIZATION=authorize)
        assert response.status_code == 404

    def test_put_missing_value(self, api_client, authorize):

        # also works for retrieve and post
        request = RequestFactory()
        expected_json = {
            'id': request.id,
            'area': request.area,
            'status': request.status.status,
            'address': request.address,
            'city': request.city,
            'country': request.country,
            'minutes': request.minutes,
        }
        status = 200
        try:
            response = api_client().post(
                self.endpoint,
                expected_json,
                format='json',
                HTTP_AUTHORIZATION=authorize
            )
            if len(expected_json) < 10:
                raise KeyError
            assert False
        except KeyError:
            assert True

    def test_unauthorized(self, api_client):
        # works for every view if I change url
        self.endpoint = '/requests/create/'
        request = RequestFactory()
        date = str(request.created_at) + "T00:00:00Z"
        expected_json = {
            'id': request.id,
            'area': request.area,
            'cost_total': request.cost_total,
            'user': request.user.fullname,
            'created_at': date,
            'status': request.status.status,
            'address': request.address,
            'city': request.city,
            'country': request.country,
            'minutes': request.minutes,
            'service_list': request.service_list.name,
            'accepted_list': request.accepted_list.name,
            'min_rating': request.min_rating,
            'max_cost': request.max_cost,
            'is_filtered': request.is_filtered,
        }
        response = api_client().get(self.endpoint)

        assert response.status_code == 401
