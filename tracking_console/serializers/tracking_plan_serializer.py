from rest_framework import serializers

from tracking_console.models.tracking_plan_model import TrackingPlanModel
from .event_configuration_serializer import EventConfigurationSerializer
from ..models import EventConfigurationTrackingPlansModel


class TrackingPlanSerializer(serializers.ModelSerializer):
    event_configurations = EventConfigurationSerializer(many=True, allow_null=False)

    class Meta:
        model = TrackingPlanModel
        fields = ("name", "description", "created_by", 'event_configurations')

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
