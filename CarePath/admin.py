from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Show role in admin and allow editing
    fieldsets = (
        *UserAdmin.fieldsets,  # Include default User fields
        ('User Role', {'fields': ('role',)}),  # Add the role field
    )

    # Add role to the user creation form
    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        ('User Role', {'fields': ('role',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
