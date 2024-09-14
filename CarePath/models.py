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
    




# class Message(models.Model):
#     recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
#     sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sent_messages')
#     subject = models.CharField(max_length=255)
#     body = models.TextField()
#     sent_at = models.DateTimeField(auto_now_add=True)
#     is_read = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.subject} - {'Read' if self.is_read else 'Unread'}"


# class Reminder(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     appointment = models.ForeignKey('Appointment', on_delete=models.CASCADE)
#     reminder_at = models.DateTimeField()

#     def __str__(self):
#         return f"Reminder for {self.appointment.patient} on {self.reminder_at}"


# class Feedback(models.Model):
#     patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
#     healthcare_provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedback_received')
#     feedback_text = models.TextField()
#     submitted_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Feedback by {self.patient} for {self.healthcare_provider}"


class Message(models.Model):
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages', null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message to {self.recipient.email} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class Feedback(models.Model):
    patient = models.ForeignKey(CustomUser, related_name='patient_feedback', on_delete=models.CASCADE)
    provider = models.ForeignKey(CustomUser, related_name='provider_feedback', on_delete=models.CASCADE)
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Feedback from {self.patient.first_name} to {self.provider.first_name} on {self.created_at}"
