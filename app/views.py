from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from .forms import RegisterForm, LoginForm
from .models import Donation, Institution, Category


class LandingPageView(View):
    def get(self, request, *args, **kwargs):
        donated_bags_sum = Donation.objects.aggregate(Sum("quantity"))["quantity__sum"]
        donated_institutions_sum = len(set(Donation.objects.values_list("institution", flat=True)))
        foundations_all = Institution.objects.filter(type="f")
        non_gov_organizations_all = Institution.objects.filter(type="ngo")
        local_collections_all = Institution.objects.filter(type="lc")
        return render(request, "index.html", {"donated_bags_sum": donated_bags_sum,
                                              "donated_institutions_sum": donated_institutions_sum,
                                              "foundations_all": foundations_all,
                                              "non_gov_organizations_all": non_gov_organizations_all,
                                              "local_collections_all": local_collections_all})


class AddDonationView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request, *args, **kwargs):
        categories_all = Category.objects.all()
        institutions_all = Institution.objects.all()
        return render(request, "form.html", {"categories_all": categories_all,
                                             "institutions_all": institutions_all})

    def post(self, request, *args, **kwargs):
        your_donation = Donation.objects.create(
            quantity=int(request.POST["bags"]),
            institution=Institution.objects.get(id=int(request.POST["organization"])),
            address=request.POST["address"],
            phone_number=request.POST["phone"],
            city=request.POST["city"],
            zip_code=request.POST["postcode"],
            pick_up_date=request.POST["data"],
            pick_up_time=request.POST["time"],
            pick_up_comment=request.POST["more_info"],
            user=request.user
            )
        selected_categories_names = request.POST.getlist("categories")
        selected_categories = Category.objects.filter(name__in=selected_categories_names)
        your_donation.categories.set(selected_categories)
        return render(request, "form-confirmation.html")


class LoginView(View):
    form = LoginForm
    html = "login.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.html, {"form": self.form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            user_exists = User.objects.filter(username=form.cleaned_data["username"]).exists()
            if user_exists:
                user = authenticate(username=form.cleaned_data["username"],
                                    password=form.cleaned_data["password"])
                if user is not None:
                    login(request, user)
                    return redirect("landing_page")
                else:
                    messages.error(request, "Invalid username or password!")
                    return render(request, self.html, {"form": self.form})
            else:
                return redirect("register")
        else:
            return render(request, self.html, {"form": self.form})



class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "register.html"
    success_url = reverse_lazy("login")


class LogoutView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("landing_page")


class UserView(LoginRequiredMixin, View):
    login_url = "login"
    html = "user.html"

    def get(self, request, *args, **kwargs):
        user_donations = Donation.objects.filter(user=self.request.user)
        user_donated_bags_sum = user_donations.aggregate(Sum("quantity"))["quantity__sum"]
        user_donated_institutions_id = user_donations.values_list("institution", flat=True)
        user_donated_institutions = Institution.objects.filter(pk__in=user_donated_institutions_id)
        user_donated_categories = Category.objects.filter(donation__in=user_donations).distinct()
        user_donations_pick_up_dates = user_donations.values_list("pick_up_date", flat=True)
        return render(request, self.html, {"user_donated_bags_sum": user_donated_bags_sum,
                                           "user_donated_institutions": user_donated_institutions,
                                           "user_donated_categories": user_donated_categories,
                                           "user_donations_pick_up_dates": user_donations_pick_up_dates})









