from django.db import models

from rudderstack.fields.base_model_fields import BaseModelFields
from tracking_console.apps import TrackingConsoleConfig as AppConfig


# Create your models here.

class TrackingPlanModel(BaseModelFields):
    name = models.CharField(null=False, blank=False, max_length=100, unique=True)
    description = models.CharField(null=False, blank=False, max_length=300)
    created_by = models.UUIDField(null=False, blank=False)

    class Meta:
        managed = True
        db_table = str(AppConfig.name) + '_tracking_plan'
        unique_together = (('name', 'created_by'), )
