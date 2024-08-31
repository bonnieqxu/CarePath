# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import CustomUser
# from django.contrib.auth.models import Group


# from django.contrib.auth.models import Group

# def create_user_groups():
#     patients_group, created = Group.objects.get_or_create(name='Patients')
#     providers_group, created = Group.objects.get_or_create(name='Healthcare Providers')
#     admins_group, created = Group.objects.get_or_create(name='Admins')
#     # 保存组
#     patients_group.save()
#     providers_group.save()
#     admins_group.save()

# # 在项目启动时调用这个函数
# create_user_groups()


# @receiver(post_save, sender=CustomUser)
# def assign_user_to_group(sender, instance, created, **kwargs):
#     if created:
#         if instance.role == 'patient':
#             group = Group.objects.get(name='Patients')
#         elif instance.role == 'provider':
#             group = Group.objects.get(name='Healthcare Providers')
#         elif instance.role == 'admin':
#             group = Group.objects.get(name='Admins')
#         group.user_set.add(instance)