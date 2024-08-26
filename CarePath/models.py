from django.db import models

# Create your models here.

from django.utils import timezone

# class LogMessage(models.Model):
#     message = models.CharField(max_length=300)
#     log_date = models.DateTimeField("date logged")

#     def __str__(self):
#         """Returns a string representation of a message."""
#         date = timezone.localtime(self.log_date)
#         return f"'{self.message}' logged on {date.strftime('%A, %d %B, %Y at %X')}"

# class Patient(models.Model):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     dob = models.DateField()
#     age = models.IntegerField()
#     phone_number = models.CharField(max_length=15)
#     email = models.EmailField(unique=True)

#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"
    

# class HealthcareProvider(models.Model):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     role = models.CharField(max_length=100)
#     department = models.CharField(max_length=100)

#     def __str__(self):
#         return f"{self.first_name} {self.last_name} - {self.role}"