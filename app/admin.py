from django.contrib import admin
from django.contrib.auth.models import User

from app.models import Institution


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "is_superuser")


class InstitutionAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "type")


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Institution, InstitutionAdmin)
