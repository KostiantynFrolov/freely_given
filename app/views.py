from django.db.models import Sum
from django.shortcuts import render
from django.views import View
from .models import Donation


class LandingPageView(View):
    def get(self, request):
        donated_bags_sum = Donation.objects.aggregate(Sum("quantity"))["quantity__sum"]
        donated_institutions_sum = len(set(Donation.objects.values_list("institution", flat=True)))
        return render(request, "index.html", {"donated_bags_sum": donated_bags_sum,
                                              "donated_institutions_sum": donated_institutions_sum})


class AddDonationView(View):
    def get(self, request):
        return render(request, "form.html")


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")


class RegisterView(View):
    def get(self, request):
        return render(request, "register.html")




