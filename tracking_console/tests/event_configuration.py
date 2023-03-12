from django.test import TestCase
from faker import Faker

from users.models import UserModel


class EventConfiguration(TestCase):
    fake: Faker = Faker()

    def setUp(self) -> None:
        self.user = UserModel.objects.create(first_name=self.fake.first_name(), last_name=self.fake.last_name(),
                                             mobile=self.fake.random_number(digits=10), email_id=self.fake.email())
        self.user.set_password(self.fake.password())
        self.user.save()

    def test_create_event_config_correct_data(self):
        from tracking_console.serializers import EventConfigurationSerializer
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
                        "product",
                        "price",
                        "currency"
                    ]
                }
            }
        })
        obj.is_valid(raise_exception=True)
        obj.save()
        self.assertIsNotNone(obj.instance.id)
