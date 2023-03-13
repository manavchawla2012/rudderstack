from rest_framework import serializers

from tracking_console.models.tracking_plan_model import TrackingPlanModel
from .event_configuration_serializer import EventConfigurationSerializer
from ..models import EventConfigurationTrackingPlansModel


class TrackingPlanSerializer(serializers.ModelSerializer):
    event_configurations = serializers.ListSerializer(child=serializers.JSONField(allow_null=False, required=True),
                                                      allow_null=False, allow_empty=True)

    class Meta:
        model = TrackingPlanModel
        fields = ("name", "description", "created_by", 'event_configurations', 'id')
        read_only_fields = ('id',)

    def to_representation(self, instance: TrackingPlanModel):
        instance.event_configurations = [config.event_config for config in
                                         instance.eventconfigurationtrackingplansmodel_set.all()]
        return super(TrackingPlanSerializer, self).to_representation(instance)

    def validate_event_configurations(self, event_configurations):
        event_configurations = [{**config, 'created_by': self.initial_data['created_by']} for config in
                                event_configurations]
        return event_configurations

    def create(self, validated_data: dict):
        from django.db import transaction
        with transaction.atomic():
            event_configurations = validated_data.pop('event_configurations')
            tracking_plan = super(TrackingPlanSerializer, self).create(validated_data)
            event_configuration_objs = EventConfigurationSerializer(data=event_configurations, many=True)
            event_configuration_objs.is_valid(raise_exception=True)
            event_configuration_objs.save()
            for event_configuration_obj in event_configuration_objs.instance:
                EventConfigurationTrackingPlansModel.objects.create(event_config=event_configuration_obj,
                                                                    tracking_plan=tracking_plan,
                                                                    created_by=validated_data['created_by'])
            tracking_plan.event_configurations = event_configuration_objs.instance
            return tracking_plan
