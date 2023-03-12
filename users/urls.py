from django.urls import path
from knox import views as knox_views

from users.views import RegisterUserView, LoginView, VerifyAuthView

UserBusinessUrls = [
    path("register", RegisterUserView.as_view(), name="register"),
    path("login", LoginView.as_view(), name="login"),
    path("logout", knox_views.LogoutView.as_view(), name="logout"),
    path("verify", VerifyAuthView.as_view(), name="verify-auth")
]
