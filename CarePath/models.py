from django.db import models

from django.utils import timezone

from django.contrib.auth.models import AbstractUser, BaseUserManager

from django.contrib import admin
from django.contrib.auth import get_user_model
from datetime import datetime




class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

# user info
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('Patient', 'Patient'),
        ('Healthcare Provider', 'Healthcare Provider'),
        ('Admin', 'Admin'),
    )

    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Disabled', 'Disabled'),
        ('Discharged', 'Discharged'),
    )

    # email is username
    username = None
    email = models.EmailField(unique=True)  
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    # Patient-specific fields
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    # Healthcare Provider-specific fields
    department = models.CharField(max_length=100, blank=True, null=True)
    provider_role = models.CharField(max_length=100, blank=True, null=True)

    status = models.CharField(max_length=20, default='Active')  # Add 'status' field to track account status
    is_active = models.BooleanField(default=True)  # Control whether the user can log in

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = []  

    objects = CustomUserManager()  # Use the custom manager

    def save(self, *args, **kwargs):
        # Ensure is_staff is correctly set based on role
        if self.role in ['Healthcare Provider', 'Admin']:
            self.is_staff = True
        else:
            self.is_staff = False
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"




# appointments
class Appointment(models.Model):
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='appointments')
    provider = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='provider_appointments')
    date = models.DateField()  # Date of the appointment
    start_time = models.TimeField()  # Start time of the appointment
    finish_time = models.TimeField()  # Finish time of the appointment
    location = models.CharField(max_length=255)  # Location of the appointment
    notes = models.TextField(blank=True, null=True)
    is_read = models.BooleanField(default=False)  # New field to track if the reminder is read or not

    def __str__(self):
        return f"Appointment for {self.patient.first_name} with {self.provider.first_name} on {self.date} at {self.start_time}"






# messages
class Message(models.Model):
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages', null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message to {self.recipient.email} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

# feedbacks
class Feedback(models.Model):
    patient = models.ForeignKey(CustomUser, related_name='patient_feedback', on_delete=models.CASCADE)
    provider = models.ForeignKey(CustomUser, related_name='provider_feedback', on_delete=models.CASCADE)
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Feedback from {self.patient.first_name} to {self.provider.first_name} on {self.created_at}"
