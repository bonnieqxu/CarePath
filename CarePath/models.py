from django.db import models

# Create your models here.

from django.utils import timezone

from django.contrib.auth.models import AbstractUser

from django.contrib import admin



# class CustomUser(AbstractUser):
#     ROLE_CHOICES = (
#         ('Patient', 'Patient'),
#         ('Healthcare Provider', 'Healthcare Provider'),
#         ('Admin', 'Admin'),
#     )

#     role = models.CharField(max_length=20, choices=ROLE_CHOICES)
#     phone_number = models.CharField(max_length=15)
#     address = models.CharField(max_length=255)

    
#     groups = models.ManyToManyField(
#         'auth.Group',
#         related_name='customuser_set',  
#         blank=True,
#         help_text='The groups this user belongs to.',
#         verbose_name='groups'
#     )
#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         related_name='customuser_set',  
#         blank=True,
#         help_text='Specific permissions for this user.',
#         verbose_name='user permissions'
#     )

#     def __str__(self):
#         return f"{self.username} ({self.get_role_display()})"

# ------------------------------------------------------------------------
# # base model
# class CustomUser(AbstractUser):
#     ROLE_CHOICES = (
#         ('Patient', 'Patient'),
#         ('Healthcare Provider', 'Healthcare Provider'),
#         ('Admin', 'Admin'),
#     )

#     role = models.CharField(max_length=20, choices=ROLE_CHOICES)
#     phone_number = models.CharField(max_length=15, blank=True, null=True)
#     address = models.CharField(max_length=255, blank=True, null=True)

#     def __str__(self):
#         return f"{self.username} ({self.get_role_display()})"
    

# # patient model
# class Patient(CustomUser):
#     date_of_birth = models.CharField(max_length=50, blank=True, null=True)

#     class Meta:
#         verbose_name = "Patient"
#         verbose_name_plural = "Patients"


# # healthcare provider model
# class HealthcareProvider(CustomUser):
#     department = models.CharField(max_length=100, blank=True, null=True)

#     class Meta:
#         verbose_name = "Healthcare Provider"
#         verbose_name_plural = "Healthcare Providers"


# # admin model
# class Admin(CustomUser):
#     class Meta:
#         verbose_name = "Admin"
#         verbose_name_plural = "Admins"

# --------------------------------------



class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('Patient', 'Patient'),
        ('Healthcare Provider', 'Healthcare Provider'),
        ('Admin', 'Admin'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    # Fields for patients
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    # Fields for healthcare providers
    department = models.CharField(max_length=100, blank=True, null=True)
    provider_role = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
