from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from rudderstack.authentication.business_authentication import BusinessAuthentication
from tracking_console.serializers import EventConfigurationSerializer, TrackingPlanSerializer, EventSerializer
from tracking_console.models import EventConfigurationModel, TrackingPlanModel, EventModel


class EventConfigLCView(ListCreateAPIView):
    queryset = EventConfigurationModel.objects
    serializer_class = EventConfigurationSerializer
    authentication_classes = (BusinessAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        request.data["created_by"] = request.user.id
        return super(EventConfigLCView, self).create(request, *args, **kwargs)


class TrackingPlanLCView(ListCreateAPIView):
    queryset = TrackingPlanModel.objects
    serializer_class = TrackingPlanSerializer
    authentication_classes = (BusinessAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        request.data["created_by"] = request.user.id
        return super(TrackingPlanLCView, self).create(request, *args, **kwargs)


class EventLCView(ListCreateAPIView):
    queryset = EventModel.objects
    serializer_class = EventSerializer
    authentication_classes = (BusinessAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        request.data["added_by"] = request.user.id
        return super(EventLCView, self).create(request, *args, **kwargs)
