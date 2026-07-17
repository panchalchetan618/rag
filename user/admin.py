from django.contrib import admin
from .models import User, UserSession


class UserSessionAdmin(admin.ModelAdmin):
    list_display = ["user__email", "jti", "expires_at", "is_active"]
    search_fields = [
        "user__email",
        "user__first_name",
        "user__last_name",
        "user__public_id",
        "jti",
    ]
    list_filter = ["expires_at", "is_active"]


class UserAdmin(admin.ModelAdmin):
    list_display = ["public_id", "email", "is_active", "email_verified", "last_login"]
    search_fields = ["first_name", "last_name", "public_id", "email"]
    list_filter = ["email_verified", "is_active", "last_login"]
    fields = [
        "public_id",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "email_verified",
        "is_superuser",
        "is_staff",
        "created_at",
        "updated_at",
        "last_login",
    ]
    readonly_fields = [
        "public_id",
        "created_at",
        "updated_at",
        "last_login",
    ]


admin.site.register(User, UserAdmin)
admin.site.register(UserSession, UserSessionAdmin)
