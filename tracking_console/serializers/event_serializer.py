from typing import List

from rest_framework import serializers

from ..dto.event_request_object import EventRequestObjectDTO
from ..models import EventModel, EventConfigurationModel


class EventSerializer(serializers.ModelSerializer):
    name = serializers.CharField(allow_null=False, allow_blank=False, write_only=True)

    class Meta:
        model = EventModel
        fields = ('data', 'added_by', 'name', 'id')
        read_only_fields = ('id', )

    def check_for_required_fields(self, fields: List[str], event_request: EventRequestObjectDTO) -> List[dict]:
        diff_fields: set = set(event_request.required_fields) - set(fields)
        errors = [{field: 'This field is required'} for field in diff_fields]
        return errors

    def check_if_fields_type_is_valid(self, data: dict, event_request: EventRequestObjectDTO) -> List[dict]:
        errors = []
        for allowed_field in event_request.allowed_fields:
            if allowed_field.field_name in data:
                for data_type in allowed_field.data_types:
                    errors.append({allowed_field.field_name: 'Invalid data type'}) if not data_type.validate(
                        data[allowed_field.field_name]) else None
        return errors

    def check_data_validation(self, data: dict, event_request: EventRequestObjectDTO) -> List[dict]:
        errors = []
        errors += self.check_for_required_fields(list(data.keys()), event_request)
        errors += self.check_if_fields_type_is_valid(data, event_request)
        return errors

    def validate_name(self, name) -> EventConfigurationModel:
        config = EventConfigurationModel.objects.filter(created_by=self.initial_data['added_by'], name=name).first()
        if not config:
            raise serializers.ValidationError({'name': 'Invalid Name for event config'})
        return config

    def validate(self, attrs: dict):
        event_config: EventConfigurationModel = attrs['name']
        attrs.pop('name')
        event_request = event_config.prepare_request_object_for_event()
        errors = self.check_data_validation(attrs['data'], event_request)
        if len(errors) > 0:
            raise serializers.ValidationError({"data": errors})
        attrs['event_configuration'] = event_config
        return attrs

    def create(self, validated_data):
        return super(EventSerializer, self).create(validated_data)
