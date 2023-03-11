from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from rudderstack.authentication.business_authentication import BusinessAuthentication
from tracking_console.serializers import EventConfigurationSerializer, TrackingPlanSerializer, EventSerializer
from tracking_console.models import EventConfigurationModel, TrackingPlanModel, EventModel


class GetUserDataMixin:
    field_name = 'created_by'

    def get_queryset(self):
        filters = {self.field_name: self.request.user.id}
        return super(GetUserDataMixin, self).get_queryset().filter(**filters)


class EventConfigLCView(GetUserDataMixin, ListCreateAPIView):
    queryset = EventConfigurationModel.objects
    serializer_class = EventConfigurationSerializer
    authentication_classes = (BusinessAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        request.data["created_by"] = request.user.id
        return super(EventConfigLCView, self).create(request, *args, **kwargs)


class TrackingPlanLCView(GetUserDataMixin, ListCreateAPIView):
    queryset = TrackingPlanModel.objects
    serializer_class = TrackingPlanSerializer
    authentication_classes = (BusinessAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        request.data["created_by"] = request.user.id
        request.data['event_configurations'] = [{**config, 'created_by': request.user.id} for config in
                                                request.data['event_configurations']]
        data = super(TrackingPlanLCView, self).create(request, *args, **kwargs)
        return data


class EventLCView(GetUserDataMixin, ListCreateAPIView):
    queryset = EventModel.objects
    serializer_class = EventSerializer
    authentication_classes = (BusinessAuthentication,)
    permission_classes = (IsAuthenticated,)
    field_name = 'added_by'

    def create(self, request, *args, **kwargs):
        request.data["added_by"] = request.user.id
        return super(EventLCView, self).create(request, *args, **kwargs)
