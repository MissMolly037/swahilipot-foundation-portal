from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Department, User


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "department",
        "role",
        "is_active",
        "is_staff",
    )

    list_filter = (
        "role",
        "department",
        "is_active",
        "is_staff",
        "is_superuser",
    )

    search_fields = (
        "username",
        "first_name",
        "last_name",
        "email",
    )

    ordering = ("username",)

    list_select_related = ("department",)

    readonly_fields = (
        "last_login",
        "date_joined",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Portal Profile",
            {
                "fields": (
                    "phone_number",
                    "profile_photo",
                    "department",
                    "role",
                    "last_session_key",
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Portal Profile",
            {
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "department",
                    "role",
                    "phone_number",
                    "profile_photo",
                )
            },
        ),
    )