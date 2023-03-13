import json

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate
from faker import Faker
from users.tests import CreateUserFactory


class TrackingConsoleAPITest(TestCase):
    fake: Faker = Faker()
    factory = APIRequestFactory()

    def setUp(self) -> None:
        self.user = CreateUserFactory.create()

    def test_create_event_config(self):
        from tracking_console.views import TrackingPlanLCView
        view = TrackingPlanLCView.as_view()
        data = {
            "name": "T6",
            "description": "T1",
            "event_configurations": [
                {
                    "name": "t5",
                    "description": "t1",
                    "rules": {
                        "schema": "http://json-schema.org/draft-07/schema#",
                        "object_type": "object",
                        "properties": {
                            "object_type": "object",
                            "properties": {
                                "product": {
                                    "data_type": [
                                        "string"
                                    ]
                                },
                                "price": {
                                    "data_type": [
                                        "number"
                                    ]
                                },
                                "currency": {
                                    "data_type": [
                                        "string"
                                    ]
                                }
                            },
                            "required": [
                                "product",
                                "price",
                                "currency"
                            ]
                        }
                    }
                }
            ]
        }
        request = self.factory.post('/api/business/tracking-console/tracking-plan', data=json.dumps(data), content_type='application/json')
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unauthorised(self):
        from tracking_console.views import TrackingPlanLCView
        view = TrackingPlanLCView.as_view()
        request = self.factory.post('/api/business/tracking-console/tracking-plan', data=json.dumps({}),
                                    content_type='application/json')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_throw_error_on_string_event_config(self):
        from tracking_console.views import TrackingPlanLCView
        view = TrackingPlanLCView.as_view()
        data = {
            "name": "T6",
            "description": "T1",
            "event_configurations": 'test'
        }
        request = self.factory.post('/api/business/tracking-console/tracking-plan', data=json.dumps(data),
                                    content_type='application/json')
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)