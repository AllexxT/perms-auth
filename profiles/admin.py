from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from profiles.models import Role

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "email",
        "date_joined",
        "last_login",
        "is_superuser",
        "is_active",
    )
    date_hierarchy = "date_joined"
    ordering = ("-date_joined",)


@admin.register(Role)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "name",
    )
    readonly_fields = ("name",)

