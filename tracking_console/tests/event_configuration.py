from django.test import TestCase
from rest_framework.serializers import ValidationError
from faker import Faker
from tracking_console.serializers import EventConfigurationSerializer
from users.tests import CreateUserFactory


class EventConfiguration(CreateUserFactory, TestCase):
    fake: Faker = Faker()

    def setUp(self) -> None:
        self.user = CreateUserFactory.create()

    # It should allow to create a event config event
    def test_create_event_config_correct_data(self):
        from tracking_console.tests.factory.event_configuration_factory import EventConfigurationFactory
        instance = EventConfigurationFactory.create()
        self.assertIsNotNone(instance.id)

    # It should throw error when required field is not part of property
    def test_event_config_required_field_not_in_property(self):
        obj = EventConfigurationSerializer(data={
            "name": self.fake.name(),
            "description": self.fake.name(),
            "created_by": self.user.id,
            "rules": {
                "schema": "http://json-schema.org/draft-07/schema#",
                "object_type": "object",
                "properties": {
                    "object_type": "object",
                    "properties": {
                        "product": {
                            "data_type": ["string"]
                        },
                        "price": {
                            "data_type": ["number"]
                        },
                        "currency": {
                            "data_type": ["string"]
                        }
                    },
                    "required": [
                        "product1",
                        "price",
                        "currency"
                    ]
                }
            }
        })
        with self.assertRaises(ValidationError):
            obj.is_valid(raise_exception=True)
            obj.save()
