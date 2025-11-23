from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin configuration for CustomUser model."""

    list_display = ('username', 'email', 'role', 'county', 'accountability_points', 'is_active')
    list_filter = ('role', 'county', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)

    fieldsets = UserAdmin.fieldsets + (
        ('Profile Information', {
            'fields': ('role', 'county', 'phone_number', 'accountability_points', 'receive_notifications')
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Profile Information', {
            'fields': ('role', 'county', 'phone_number')
        }),
    )
