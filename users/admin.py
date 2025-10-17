from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    readonly_fields = ("created_time", "last_login", "date_joined")
    
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Informations personnelles", {"fields": ("birthday", "can_be_contacted", "can_data_be_shared")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Dates importantes", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("username", "password1", "password2", "birthday", "can_be_contacted", "can_data_be_shared")}),
    )
    list_display = ("id", "username", "birthday", "can_be_contacted", "is_staff", "is_active")
    search_fields = ("username",)
    ordering = ("username",)
