from django.urls import path
from .views import (LandingPageView, AddDonationView, LoginView, RegisterView,
                    LogoutView, UserPageView, PasswordConfirmView, ChangeUserDataView,
                    ChangeUserPasswordView)

urlpatterns = [
    path("", LandingPageView.as_view(), name="landing_page"),
    path("add-donation/", AddDonationView.as_view(), name="add_donation"),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("user-page/", UserPageView.as_view(), name="user_page"),
    path("password-confirm/", PasswordConfirmView.as_view(), name="password_confirm"),
    path("change-user-data/", ChangeUserDataView.as_view(), name="change_user_data"),
    path("change-user-password/", ChangeUserPasswordView.as_view(), name="change_user_password")
]