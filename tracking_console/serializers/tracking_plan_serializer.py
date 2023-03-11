from rest_framework import serializers

from tracking_console.models.tracking_plan_model import TrackingPlanModel


class TrackingPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackingPlanModel
        fields = ("name", "description", "created_by")
