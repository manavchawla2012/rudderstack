from faker import Faker

from users.tests import CreateUserFactory


class EventConfigurationFactory:

    @staticmethod
    def create():
        fake: Faker = Faker()
        user = CreateUserFactory.create()
        from tracking_console.serializers import EventConfigurationSerializer
        obj = EventConfigurationSerializer(data={
            "name": fake.name(),
            "description": fake.name(),
            "created_by": user.id,
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
        return obj.instance
