from django.urls import path
from .views import LandingPageView, AddDonationView, LoginView, RegisterView, LogoutView

urlpatterns = [
    path("", LandingPageView.as_view(), name="landing_page"),
    path("add-donation/", AddDonationView.as_view(), name="add_donation"),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout")
]