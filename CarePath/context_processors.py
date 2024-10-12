from django.contrib.messages import get_messages
from datetime import date, timedelta
from .models import Message, Appointment, Feedback, CustomUser

def unread_counts(request):
    if request.user.is_authenticated:

        unread_messages_count = Message.objects.filter(recipient=request.user, is_read=False).count()


        today = date.today()
        reminders = Appointment.objects.filter(
            patient=request.user,
            date__range=[today, today + timedelta(days=3)]
        )


        unread_reminders_count = Appointment.objects.filter(
            patient=request.user,
            is_read=False,
            date__range=[today, today + timedelta(days=3)]
        ).count()

        return {
            'unread_messages_count': unread_messages_count,
            'unread_reminders_count': unread_reminders_count,
        }
    else:
        return {
            'unread_messages_count': 0,
            'unread_reminders_count': 0,
        }




def unread_notifications(request):
    if request.user.is_authenticated:
        today = date.today()
        unread_feedback_count = 0
        unread_messages_count = 0
        unread_reminders_count = 0
        pending_users_count = 0

        if request.user.role == 'Healthcare Provider':
            unread_feedback_count = Feedback.objects.filter(provider=request.user, is_read=False).count()
        elif request.user.role == 'Patient':
            unread_messages_count = Message.objects.filter(recipient=request.user, is_read=False).count()
            unread_reminders_count = Appointment.objects.filter(patient=request.user, date__gte=today).count()
        elif request.user.role == 'Admin':
            # For admin, calculate pending users and unread feedback
            pending_users_count = CustomUser.objects.filter(role='Healthcare Provider', status='Disabled').count()
            unread_feedback_count = Feedback.objects.filter(provider=request.user, is_read=False).count()


        return {
            'unread_feedback_count': unread_feedback_count,
            'unread_messages_count': unread_messages_count,
            'unread_reminders_count': unread_reminders_count,
            'pending_users_count': pending_users_count,
        }
    return {}
