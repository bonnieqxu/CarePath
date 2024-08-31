from django import forms
from .models import CustomUser
from django.contrib.auth.models import Group

# from CarePath.models import LogMessage

# class LogMessageForm(forms.ModelForm):
#     class Meta:
#         model = LogMessage
#         fields = ("message",)   # NOTE: the trailing comma is required


# class RegisterForm(forms.ModelForm):
#     role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=True)

#     class Meta:
#         model = CustomUser
#         fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'address', 'password', 'role']
#         widgets = {
#             'password': forms.PasswordInput(),
#         }

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data['password'])  # 确保密码被加密

#         if commit:
#             user.save()
#             # 分配用户组
#             if user.role == 'patient':
#                 patients_group = Group.objects.get(name='Patients')
#                 patients_group.user_set.add(user)
#             elif user.role == 'provider':
#                 providers_group = Group.objects.get(name='Healthcare Providers')
#                 providers_group.user_set.add(user)
#             elif user.role == 'admin':
#                 admins_group = Group.objects.get(name='Admins')
#                 admins_group.user_set.add(user)

#         return user