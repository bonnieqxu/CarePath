from django.db import models

# Create your models here.

from django.utils import timezone

from django.contrib.auth.models import AbstractUser

from django.contrib import admin
from django.contrib.auth import get_user_model
from datetime import datetime




# user info
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
    




# appointments
class Appointment(models.Model):
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='appointments')
    provider = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='provider_appointments')
    date = models.DateField()  # Date of the appointment
    start_time = models.TimeField()  # Start time of the appointment
    finish_time = models.TimeField()  # Finish time of the appointment
    location = models.CharField(max_length=255)  # Location of the appointment
    notes = models.TextField(blank=True, null=True)

    @property
    def duration(self):
        # Calculate the duration from start_time to finish_time
        start_dt = datetime.combine(self.date, self.start_time)
        finish_dt = datetime.combine(self.date, self.finish_time)
        return finish_dt - start_dt

    def __str__(self):
        return f"Appointment for {self.patient.first_name} with {self.provider.first_name} on {self.date} at {self.start_time}"