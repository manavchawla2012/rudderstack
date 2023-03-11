from rudderstack.fields.base_model_fields import BaseModelFields, models
from . import EventConfigurationModel
from ..apps import TrackingConsoleConfig as AppConfig


class EventModel(BaseModelFields):
    event_configuration = models.ForeignKey(EventConfigurationModel, null=False, blank=False,
                                            on_delete=models.DO_NOTHING)
    data = models.JSONField(null=False, blank=False)
    added_by = models.UUIDField(null=False, blank=False)

    class Meta:
        managed = True
        db_table = str(AppConfig.name) + '_event'
