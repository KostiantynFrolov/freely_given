from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView, PasswordChangeView
from django.db.models import Sum
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import translation
from django.views import View
from django.views.generic import CreateView, FormView, UpdateView

from .forms import LoginForm, PasswordConfirmForm, RegisterForm
from .emails import send_confirmational_email
from .models import Category, Donation, Institution


class LandingPageView(View):
    def get(self, request, *args, **kwargs):
        donated_bags_sum = Donation.objects.aggregate(Sum("quantity"))["quantity__sum"]
        donated_institutions_sum = (Donation.objects.
                                    values("institution_id").distinct().count())
        foundations_all = Institution.objects.filter(type="f")
        non_gov_organizations_all = Institution.objects.filter(type="ngo")
        local_collections_all = Institution.objects.filter(type="lc")
        return render(request, "index.html",
                      {"donated_bags_sum": donated_bags_sum,
                       "donated_institutions_sum": donated_institutions_sum,
                       "foundations_all": foundations_all,
                       "non_gov_organizations_all": non_gov_organizations_all,
                       "local_collections_all": local_collections_all})


class AddDonationView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request, *args, **kwargs):
        categories_all = Category.objects.all()
        institutions_all = Institution.objects.all()
        return render(request, "form.html",
                      {"categories_all": categories_all,
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
        selected_categories = (Category.objects.
                               filter(name__in=selected_categories_names))
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
            user_exists = (User.objects.
                           filter(username=form.cleaned_data["username"]).exists())
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
    success_url = reverse_lazy("landing_page")

    def get(self, request, *args, **kwargs):
        translation.activate("pl")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        translation.activate("pl")
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        send_confirmational_email(self.object)
        return response


class LogoutView_(LogoutView):
    next_page = reverse_lazy("landing_page")


class UserPageView(LoginRequiredMixin, View):
    login_url = "login"
    html = "user_page.html"

    def get(self, request, *args, **kwargs):
        user_donations = Donation.objects.filter(user=self.request.user)
        return render(request, self.html, {"user_donations": user_donations})

    def post(self, request, *args, **kwargs):
        user_donation = Donation.objects.get(pk=request.POST["don_id"])
        user_donation.is_taken = True if request.POST["status"] == "False" else False
        user_donation.save()
        user_donations = Donation.objects.filter(user=self.request.user)
        return render(request, self.html, {"user_donations": user_donations})


class PasswordConfirmView(LoginRequiredMixin, FormView):
    form_class = PasswordConfirmForm
    template_name = "password-confirm.html"

    def form_valid(self, form):
        password = form.cleaned_data.get("password")
        user = self.request.user
        if check_password(password, user.password):
            return render(self.request, "changes_choice.html")
        else:
            messages.error(self.request, "Nieprawidłowe hasło. Spróbuj ponownie.")
            return self.form_invalid(form)


class ChangeUserDataView(LoginRequiredMixin, UpdateView):
    login_url = "login"
    model = User
    fields = ["username", "first_name", "last_name"]
    template_name = "change_user_data.html"
    success_url = reverse_lazy("user_page")

    def get_object(self, queryset=None):
        return self.request.user


class ChangeUserPasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = "change_user_password.html"
    success_url = reverse_lazy("user_page")

    def get(self, request, *args, **kwargs):
        translation.activate("pl")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        translation.activate("pl")
        return super().post(request, *args, **kwargs)
