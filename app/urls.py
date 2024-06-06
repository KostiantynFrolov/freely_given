from django.urls import path

from .views import (AddDonationView, ChangeUserDataView,
                    ChangeUserPasswordView, LandingPageView, LoginView,
                    LogoutView_, PasswordConfirmView, RegisterView,
                    UserPageView, AccountActivationView, ForgotPasswordView,
                    ResetPasswordView)

urlpatterns = [
    path("", LandingPageView.as_view(), name="landing_page"),
    path("add-donation/", AddDonationView.as_view(), name="add_donation"),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView_.as_view(), name="logout"),
    path("user-page/", UserPageView.as_view(), name="user_page"),
    path("password-confirm/", PasswordConfirmView.as_view(), name="password_confirm"),
    path("change-user-data/", ChangeUserDataView.as_view(), name="change_user_data"),
    path("change-user-password/",
         ChangeUserPasswordView.as_view(),
         name="change_user_password"),
    path("account-activation/<uid>/<token>/",
         AccountActivationView.as_view(),
         name="account_activation"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot_password"),
    path("reset-password/<uid>/<token>/",
         ResetPasswordView.as_view(),
         name="reset_password")
]
