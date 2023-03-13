from django.urls import path

from tracking_console.views import EventConfigLCView, TrackingPlanLCView, EventLCView, TrackingPlanReadView

urlpatterns = [
    path('event-configuration', EventConfigLCView.as_view(), name='event_configuration'),
    path('tracking-plan', TrackingPlanLCView.as_view(), name='tracking_plan'),
    path('tracking-plan/<uuid:id>', TrackingPlanReadView.as_view(), name='tracking_plan_rud'),
    path('event', EventLCView.as_view(), name='event'),
]
