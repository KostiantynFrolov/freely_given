import pytest
from django.contrib.auth.hashers import check_password
from app.models import Category, Institution, Donation


@pytest.mark.django_db
def test_category_model(category_1):
    assert Category.objects.count() == 1
    categ = Category.objects.get(name="Test category")
    assert categ == category_1
    assert categ.name == "Test category"
    assert str(categ) == "Test category"

@pytest.mark.django_db
def test_institution_model_1(institution_1, category_1):
    assert Institution.objects.count() == 1
    instit = Institution.objects.get(name="Test institution")
    assert instit == institution_1
    assert instit.name == "Test institution"
    assert instit.description == "Test institution description"
    assert instit.type == "f"
    assert instit.categories.all().count() == 1
    assert category_1 in instit.categories.all()
    assert str(instit) == "Test institution"

@pytest.mark.django_db
def test_institution_model_2(institution_2, category_1, category_2):
    assert Institution.objects.count() == 1
    instit = Institution.objects.get(name="Test institution 2")
    assert instit == institution_2
    assert instit.name == "Test institution 2"
    assert instit.description == "Test institution description 2"
    assert instit.type == Institution.FOUNDATION
    assert instit.categories.all().count() == 2
    assert category_1 in instit.categories.all()
    assert category_2 in instit.categories.all()
    assert str(instit) == "Test institution 2"

@pytest.mark.django_db
def test_institution_model_3(institution_3):
    instit = Institution.objects.get(name="Test institution 3")
    assert instit.categories.all().count() == 3
    assert instit.type == "ngo"

@pytest.mark.django_db
def test_institution_model_4(institution_4):
    instit = Institution.objects.get(name="Test institution 4")
    assert instit.type == "lc"

@pytest.mark.django_db
def test_donation_model_1(category_1, institution_1, donation_1):
    assert Donation.objects.count() == 1
    donat = Donation.objects.all().first()
    assert donat == donation_1
    assert donat.categories.all().count() == 1
    assert category_1 in donat.categories.all()
    assert donat.institution == institution_1
    assert donat.quantity == 1
    assert donat.address == "Some address"
    assert donat.phone_number == "123-456-789"
    assert donat.city == "Warsaw"
    assert donat.zip_code == "123-456"
    assert donat.pick_up_date.strftime("%Y-%m-%d") == "2024-05-23"
    assert donat.pick_up_time.strftime("%H:%M") == "17:17"
    assert donat.pick_up_comment == "Don't late"
    assert donat.is_taken is False
    assert donat.user is None

@pytest.mark.django_db
def test_donation_model_2(category_1, category_2, institution_2, user, donation_2):
    assert Donation.objects.count() == 1
    donat = Donation.objects.all().first()
    assert donat == donation_2
    assert donat.categories.all().count() == 2
    assert category_1 in donat.categories.all()
    assert category_2 in donat.categories.all()
    assert donat.institution == institution_2
    assert donat.quantity == 2
    assert donat.address == "Some address"
    assert donat.phone_number == "123-456-789"
    assert donat.city == "Warsaw"
    assert donat.zip_code == "123-456"
    assert donat.pick_up_date.strftime("%Y-%m-%d") == "2024-05-24"
    assert donat.pick_up_time.strftime("%H:%M") == "17:07"
    assert donat.pick_up_comment == "No comment"
    assert donat.user == user
    assert donat.user.first_name == "Kostek"
    assert donat.user.last_name == "Frolov"
    assert donat.user.username == "konst050383@gmail.com"
    assert check_password("Testing01!", user.password)
    assert donat.is_taken is False

@pytest.mark.django_db
def test_three_donations(donation_1, donation_3):
    assert Donation.objects.all().first() == donation_1
    assert Donation.objects.all().last() == donation_3

@pytest.mark.django_db
def test_four_donations(donation_1, donation_2, donation_3, donation_4):
    assert Donation.objects.all()[2] == donation_3
    assert Donation.objects.all().last() == donation_4






