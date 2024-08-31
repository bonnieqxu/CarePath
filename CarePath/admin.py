from django.contrib import admin

# Register your models here.
# from .models import CustomUser
# from django.contrib.auth.models import Group, Permission
# from django.contrib.contenttypes.models import ContentType
# from .models import User

# def create_user_groups():
    
#     patients_group, created = Group.objects.get_or_create(name='Patients')
#     providers_group, created = Group.objects.get_or_create(name='Healthcare Providers')
#     admins_group, created = Group.objects.get_or_create(name='Admins')

#     # 为不同的组分配权限（可选）
#     # permission = Permission.objects.get(codename='add_user')  # 示例权限
#     # patients_group.permissions.add(permission)
#     # providers_group.permissions.add(permission)
#     # admins_group.permissions.add(permission)

#     # 保存组
#     patients_group.save()
#     providers_group.save()
#     admins_group.save()


# @admin.register(CustomUser)
# class CustomUserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')
#     list_filter = ('role', 'is_staff', 'is_active')
#     search_fields = ('username', 'email', 'first_name', 'last_name')
#     ordering = ('username',)

#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'address')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#         ('Role Information', {'fields': ('role',)}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'password1', 'password2', 'role', 'is_staff', 'is_active'),
#         }),
#     )

# admin.site.register(Group)
# admin.site.register(Permission)
