from django.urls import path

from tracking_console.views import EventConfigLCView, TrackingPlanLCView, EventLCView

urlpatterns = [
    path('event-configuration', EventConfigLCView.as_view(), name='event_configuration'),
    path('tracking-plan', TrackingPlanLCView.as_view(), name='tracking_plan'),
    path('event', EventLCView.as_view(), name='event'),
]
