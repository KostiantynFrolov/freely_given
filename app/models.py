from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)


class Institution(models.Model):
    FOUNDATION = "f"
    NON_GOVERNMENT_ORGANIZATION = "ngo"
    LOCAL_COLLECTION = "lc"
    TYPES = [
        (FOUNDATION, "foundation"),
        (NON_GOVERNMENT_ORGANIZATION, "non-government organization"),
        (LOCAL_COLLECTION, "local collection")
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=10, choices=TYPES, default=TYPES[0][0])
    categories = models.ManyToManyField(Category)


class Donation(models.Model):
    quantity = models.SmallIntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=30)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)
