from typing import List

from django.db import models

from rudderstack.fields.base_model_fields import BaseModelFields
from tracking_console.apps import TrackingConsoleConfig as AppConfig
from tracking_console.dto.event_request_object import EventRequestObjectDTO, FieldDTO


class EventConfigurationModel(BaseModelFields):
    name = models.CharField(null=False, blank=False, max_length=100, unique=True)
    description = models.CharField(null=False, blank=False, max_length=300)
    rules = models.JSONField(null=False, blank=False)
    created_by = models.UUIDField(null=False, blank=False)

    class Meta:
        managed = True
        db_table = str(AppConfig.name) + '_event_configuration'
        unique_together = (('name', 'created_by'),)

    def prepare_request_object_for_event(self) -> EventRequestObjectDTO:
        properties = self.rules["properties"]
        required_fields = properties["required"]
        from tracking_console.enum import DataTypeEnum
        allowed_fields: List[FieldDTO] = []
        for property_key, value in properties["properties"].items():
            allowed_fields.append(
                FieldDTO(property_key, [DataTypeEnum.search_by_value(key) for key in value['data_type']]))
        return EventRequestObjectDTO(required_fields=required_fields, allowed_fields=allowed_fields)
