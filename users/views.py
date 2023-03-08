from django.contrib.auth import login

from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from knox.views import LoginView as KnoxLoginView

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
