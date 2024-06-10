from django.contrib import admin
from django.contrib.auth.models import User

from app.models import Institution


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "is_superuser")

    def has_delete_permission(self, request, obj=None):
        superusers_quantity = User.objects.filter(is_superuser=True).count()
        if superusers_quantity <= 1:
            if obj is not None and obj.is_superuser:
                return False
        return super().has_delete_permission(request, obj)


class InstitutionAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "type")


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Institution, InstitutionAdmin)
