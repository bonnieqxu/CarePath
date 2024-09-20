from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# class CustomUserAdmin(UserAdmin):
#     model = CustomUser
#     # Show role in admin and allow editing
#     fieldsets = (
#         *UserAdmin.fieldsets,  # Include default User fields
#         ('User Role', {'fields': ('role',)}),  # Add the role field
#     )

#     # Add role to the user creation form
#     add_fieldsets = (
#         *UserAdmin.add_fieldsets,
#         ('User Role', {'fields': ('role',)}),
#     )

# admin.site.register(CustomUser, CustomUserAdmin)


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    ordering = ['email']
    
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'status')
    search_fields = ('email', 'first_name', 'last_name')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number', 'address', 'date_of_birth')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Role & Status', {'fields': ('role', 'status', 'department', 'provider_role')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)