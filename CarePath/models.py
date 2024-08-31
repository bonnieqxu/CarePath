from django.db import models

# Create your models here.

from django.utils import timezone

from django.contrib.auth.models import AbstractUser

from django.contrib import admin



class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('Patient', 'Patient'),
        ('Healthcare Provider', 'Healthcare Provider'),
        ('Admin', 'Admin'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)

    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # 指定 related_name 以避免冲突
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # 指定 related_name 以避免冲突
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
