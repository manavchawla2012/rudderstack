from rudderstack.fields.base_model_fields import BaseModelFields, models
from . import EventConfigurationModel, TrackingPlanModel
from ..apps import TrackingConsoleConfig as AppConfig


class EventConfigurationTrackingPlansModel(BaseModelFields):
    event_config = models.ForeignKey(EventConfigurationModel, null=False, blank=False, on_delete=models.CASCADE)
    tracking_plan = models.ForeignKey(TrackingPlanModel, null=False, blank=False, on_delete=models.CASCADE)
    created_by = models.UUIDField(null=False, blank=False)

    class Meta:
        managed = True
        db_table = str(AppConfig.name) + '_event_configuration_tracking_plans'
        unique_together = (('event_config_id', 'tracking_plan_id'),)
