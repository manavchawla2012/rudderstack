from django.contrib.auth import login

from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from knox.views import LoginView as KnoxLoginView
from rest_framework.response import Response

from rudderstack.authentication.business_authentication import BusinessAuthentication
from users.models import UserModel
from users.serializers import RegisterUserSerializer


class RegisterUserView(CreateAPIView):
    queryset = UserModel.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterUserSerializer


class LoginView(KnoxLoginView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: UserModel = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class VerifyAuthView(GenericAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = (BusinessAuthentication, )

    def get(self, *args, **kwargs):
        return Response({"is_authenticated": self.request.user.is_authenticated})
