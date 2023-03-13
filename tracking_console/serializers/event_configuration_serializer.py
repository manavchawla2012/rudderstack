from typing import List

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from ..enum import RuleTypeEnum, DataTypeEnum
from ..models import EventConfigurationModel


class PropertyFieldSerializer(serializers.Serializer):
    data_type = serializers.ListField(
        child=serializers.ChoiceField(allow_null=False, allow_blank=False, choices=DataTypeEnum.get_choices()),
        allow_empty=False)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class PropertiesSerializer(serializers.Serializer):
    object_type = serializers.ChoiceField(allow_blank=False, allow_null=False, choices=RuleTypeEnum.get_choices())
    properties = serializers.JSONField(allow_null=False, required=True)
    required = serializers.ListSerializer(
        child=serializers.CharField(allow_null=False, allow_blank=False, required=True), allow_null=False,
        allow_empty=True)

    def validate_properties(self, properties: dict):
        for key, value in properties.items():
            obj = PropertyFieldSerializer(data=value)
            obj.is_valid(raise_exception=True)
        return properties

    def check_if_required_fields_in_properties(self, required_fields: List[str], properties: dict):
        diff_keys = set(required_fields) - set(properties.keys())
        if len(diff_keys) > 0:
            raise serializers.ValidationError(
                {"required": [{key: f"{key} required key is not present in property"} for key in diff_keys]})

    def validate(self, attrs):
        if not self.instance:
            self.check_if_required_fields_in_properties(attrs["required"], attrs["properties"])
        return super(PropertiesSerializer, self).validate(attrs)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class RuleSerializer(serializers.Serializer):
    schema = serializers.URLField(allow_blank=False, allow_null=False, required=True)

    object_type = serializers.ChoiceField(allow_blank=False, allow_null=False, choices=RuleTypeEnum.get_choices())
    properties = PropertiesSerializer(allow_null=False, required=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class EventConfigurationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(allow_null=False, allow_blank=False, required=True,
                                 validators=[UniqueValidator(EventConfigurationModel.objects)])
    description = serializers.CharField(allow_null=False, allow_blank=False, required=True)
    rules = RuleSerializer(allow_null=False, required=True)
    created_by = serializers.UUIDField(required=False)

    class Meta:
        model = EventConfigurationModel
        fields = ("name", "description", "rules", "id", "created_by")
        extra_kwargs = {"created_by": {"required": False, "allow_null": True}}