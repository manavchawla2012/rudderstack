import json

from django.test import TestCase
from faker import Faker
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from users.models import UserModel


class EventAPITest(TestCase):
    fake: Faker = Faker()
    factory = APIRequestFactory()

    def setUp(self) -> None:
        from tracking_console.tests import EventConfigurationFactory
        from tracking_console.models import EventConfigurationModel
        self.config: EventConfigurationModel = EventConfigurationFactory.create()
        self.user = UserModel.objects.first()

    def test_submit_success_event(self):
        data = {
            "data": {
                "product": "Item1",
                "currency": "Dollar",
                "price": "10"
            },
            "name": self.config.name
        }
        response = self.create_event(data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_when_invalid_property_passed(self):
        data = {
            "data": {
                "product": "Item1",
                "currency": "Dollar",
                "price1": "10"
            },
            "name": self.config.name
        }
        response = self.create_event(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_when_required_field_is_not_passed(self):
        data = {
            "data": {
                "product": "Item1",
                "currency": "Dollar",
            },
            "name": self.config.name
        }
        response = self.create_event(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_when_required_wrong_data_type_is_passed(self):
        data = {
            "data": {
                "product": "Item1",
                "currency": "Dollar",
                "price": "price"
            },
            "name": self.config.name
        }
        response = self.create_event(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def create_event(self, data):
        from tracking_console.views import EventLCView
        view = EventLCView.as_view()
        request = self.factory.post('/api/business/tracking-console/event', data=json.dumps(data),
                                    content_type='application/json')
        force_authenticate(request, user=self.user)
        response = view(request)
        return response
