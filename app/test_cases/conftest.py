import pytest
from django.contrib.auth.models import User
from app.models import Category, Institution, Donation


@pytest.fixture
def category_1():
    return Category.objects.create(name="Test category")

@pytest.fixture
def category_2():
    return Category.objects.create(name="Test category 2")

@pytest.fixture
def category_3():
    return Category.objects.create(name="Test category 3")

@pytest.fixture
def institution_1(category_1):
    institution_test = Institution.objects.create(
        name="Test institution",
        description="Test institution description",
        type="f")
    institution_test.categories.add(category_1)
    return institution_test

@pytest.fixture
def institution_2(category_1, category_2):
    institution_test = Institution.objects.create(
        name="Test institution 2",
        description="Test institution description 2")
    institution_test.categories.add(category_1, category_2)
    return institution_test

@pytest.fixture
def institution_3(category_1, category_2, category_3):
    institution_test = Institution.objects.create(
        name="Test institution 3",
        description="Test institution description 3",
        type="ngo")
    institution_test.categories.add(category_1, category_2, category_3)
    return institution_test

@pytest.fixture
def institution_4(category_3):
    institution_test = Institution.objects.create(
        name="Test institution 4",
        description="Test institution description 4",
        type="lc")
    institution_test.categories.add(category_3)
    return institution_test

@pytest.fixture
def donation_1(category_1, institution_1):
    donation_test = Donation.objects.create(
        quantity=1,
        institution=institution_1,
        address="Some address",
        phone_number="123-456-789",
        city="Warsaw",
        zip_code="123-456",
        pick_up_date="2024-05-23",
        pick_up_time="17:17",
        pick_up_comment="Don't late",
        is_taken=False
    )
    donation_test.categories.add(category_1)
    return donation_test

@pytest.fixture
def user():
    user_test = User.objects.create(
        first_name="Kostek",
        last_name="Frolov",
        username="konst050383@gmail.com",
    )
    user_test.set_password("Testing01!")
    user_test.save()
    return user_test

@pytest.fixture
def donation_2(category_1, category_2, institution_2, user):
    donation_test = Donation.objects.create(
        quantity=2,
        institution=institution_2,
        address="Some address",
        phone_number="123-456-789",
        city="Warsaw",
        zip_code="123-456",
        pick_up_date="2024-05-24",
        pick_up_time="17:07",
        pick_up_comment="No comment",
        user=user,
        is_taken=False
    )
    donation_test.categories.add(category_1, category_2)
    return donation_test

@pytest.fixture
def donation_3(category_2, institution_2, user):
    donation_test = Donation.objects.create(
        quantity=3,
        institution=institution_2,
        address="Some address",
        phone_number="123-456-789",
        city="Warsaw",
        zip_code="123-456",
        pick_up_date="2024-05-23",
        pick_up_time="18:18",
        pick_up_comment="No comment",
        user=user,
        is_taken=True
    )
    donation_test.categories.add(category_2)
    return donation_test

@pytest.fixture
def donation_4(category_1, category_2, category_3, institution_3, user):
    donation_test = Donation.objects.create(
        quantity=4,
        institution=institution_3,
        address="Some address",
        phone_number="123-456-789",
        city="Warsaw",
        zip_code="123-456",
        pick_up_date="2024-05-24",
        pick_up_time="17:17",
        pick_up_comment="See you!",
        user=user,
        is_taken=True
    )
    donation_test.categories.add(category_1, category_2, category_3)
    return donation_test





