import re
import os
from datetime import date, time

from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import password_validators_help_texts
from django.views.generic import TemplateView
from django.contrib.auth.models import Group
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm

from django.utils import timezone
from django.utils.timezone import datetime
from django.utils.translation import gettext as _

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from .models import CustomUser, Appointment
from django.db.models import Q






User = get_user_model()

#----------------------- VISITOR related views  -------------------------------

# landing page
def home(request):
    return render(request, 'CarePath/home.html')



# Treatment journey related views
def journey(request):
    return render(request, "CarePath/journey.html")

def mdm(request):
    return render(request, "CarePath/mdm.html")

def pre_dental(request):
    return render(request, "CarePath/pre_dental.html")

def tx_sideeffect(request):
    return render(request, "CarePath/tx_sideeffect.html")

def mucositis(request):
    return render(request, "CarePath/mucositis.html")

def post_dental(request):
    return render(request, "CarePath/post_dental.html")

def discharge(request):
    return render(request, "CarePath/discharge.html")



# informative materials related views
def info(request):
    return render(request, "CarePath/info.html")

def mouthcare(request):
    return render(request, "CarePath/mouthcare.html")

# download a mouthcare pdf
def mouthcare_pdf(request):
    file_path = os.path.join(settings.BASE_DIR, 'CarePath', 'static', 'CarePath', 'pdf', 'mouthcare.pdf')
    with open(file_path, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="mouthcare.pdf"'
        return response
    
def drymouth(request):
    return render(request, "CarePath/drymouth.html")
    
# download a drymouth pdf
def drymouth_pdf(request):
    file_path = os.path.join(settings.BASE_DIR, 'CarePath', 'static', 'CarePath', 'pdf', 'drymouth.pdf')
    with open(file_path, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="drymouth.pdf"'
        return response

def sideeffect(request):
    return render(request, "CarePath/sideeffect.html")

# download a side effect pdf
def sideeffect_pdf(request):
    file_path = os.path.join(settings.BASE_DIR, 'CarePath', 'static', 'CarePath', 'pdf', 'sideeffects.pdf')
    with open(file_path, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="sideeffects.pdf"'
        return response

def speech(request):
    return render(request, "CarePath/speech.html")

# downland a swallowing exercise
def speech_pdf(request):
    file_path = os.path.join(settings.BASE_DIR, 'CarePath', 'static', 'CarePath', 'pdf', 'SLT Swallowing exercise.pdf')
    with open(file_path, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="SLT Swallowing exercise.pdf"'
        return response

# download a trismus exercise
def stretch_pdf(request):
    file_path = os.path.join(settings.BASE_DIR, 'CarePath', 'static', 'CarePath', 'pdf', 'SLT Trismus exersice.pdf')
    with open(file_path, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="SLT Trismus exersice.pdf"'
        return response

def diet(request):
    return render(request, "CarePath/diet.html")

# download a diet pdf
def diet_pdf(request):
    file_path = os.path.join(settings.BASE_DIR, 'CarePath', 'static', 'CarePath', 'pdf', 'Poor Appetite.pdf')
    with open(file_path, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Poor Appetite.pdf"'
        return response

def mouthcare_post(request):
    return render(request, "CarePath/mouthcare_post.html")

# download a post treatment mouthcare info pdf
def mouthcare_post_pdf(request):
    file_path = os.path.join(settings.BASE_DIR, 'CarePath', 'static', 'CarePath', 'pdf', 'mouthcare_post.pdf')
    with open(file_path, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="mouthcare_post.pdf"'
        return response




# clinician related views
def team(request):
    return render(request, "CarePath/team.html")




# register a new account
# def register(request):
#     if request.method == "POST":
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         phone_number = request.POST['phone_number']
#         email = request.POST['email']
#         address = request.POST['address']
#         password = request.POST['password']
#         confirm_password = request.POST['confirm_password']
#         role = request.POST['role']

#         if password != confirm_password:
#             return render(request, 'CarePath/register.html', {'error': "Passwords do not match"})

#         if CustomUser.objects.filter(email=email).exists():
#             return render(request, 'CarePath/register.html', {'error': "Email already in use"})

#         # Create the new user
#         user = CustomUser.objects.create_user(
#             username=email,  # email is used as the username
#             email=email,
#             first_name=first_name,
#             last_name=last_name,
#             phone_number=phone_number,
#             address=address,
#             password=password,
#             role=role,
#         )

#         user.save()
#         group = Group.objects.get(name=role)
#         user.groups.add(group)

#         return redirect('login')  # Redirect to the login page after successful registration

#     return render(request, 'CarePath/register.html')





def register(request):
    today_date = date.today().strftime('%Y-%m-%d')  # Format today's date as YYYY-MM-DD
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        role = request.POST['role']

         # For patients only
        date_of_birth = request.POST.get('date_of_birth', None)
        address = request.POST.get('address', None)

        # for providers only
        department = request.POST.get('department', None)
        provider_role = request.POST.get('provider_role', None)


        # Check if passwords match
        if password != confirm_password:
            return render(request, 'CarePath/register.html', {'error': "Passwords do not match"})

        # Check if email is already in use
        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'CarePath/register.html', {'error': "Email already in use"})

        # Ensure Admin registration is only possible via Django Admin or superuser
        if role == 'Admin':
            return render(request, 'CarePath/register.html', {'error': "Admin registration is not allowed via this form."})

        # Create the new user with the selected role (Patient or Healthcare Provider)
        user = CustomUser.objects.create_user(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            password=password,
            role=role,
        )

        # Set additional fields for patients
        if role == 'Patient':
            # user.date_of_birth = date_of_birth
            # user.address = address
            if date_of_birth:  # Only set date_of_birth if it is provided
                user.date_of_birth = date_of_birth
            if address:
                user.address = address

        if role == 'Healthcare Provider':
            # user.department = department
            # user.provider_role = provider_role
            if department:
                user.department = department
            if provider_role:
                user.provider_role = provider_role

        user.save()
        
        # Assign the user to the appropriate group based on the role
        group = Group.objects.get(name=role)
        user.groups.add(group)

        return redirect('login')  # Redirect to login after successful registration

    return render(request, 'CarePath/register.html', {'today_date': today_date})









# --------------------------------- REGISTERED USER VIEWS ------------------------

# user login
def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)

        if user is not None:
            auth_login(request, user)

            # log into role appropriate Dashboard
            if user.role == 'Patient':
                return redirect('patient_dashboard')
            elif user.role == 'Healthcare Provider':
                return redirect('provider_dashboard')
            elif user.role == 'Admin':
                return redirect('admin_dashboard')
        else:
            # return error message
            messages.error(request, 'Invalid email or password.')
            return redirect('login')
        
    return render(request, "CarePath/login.html")


# # dashboards
@login_required
def patient_dashboard(request):
    return render(request, 'CarePath/patient_dashboard.html')

@login_required
def provider_dashboard(request):
    return render(request, 'CarePath/provider_dashboard.html')

@login_required
def admin_dashboard(request):
    return render(request, 'CarePath/admin_dashboard.html')


@login_required
def dashboard(request):
    if request.user.role == 'Patient':
        return redirect('patient_dashboard')
    elif request.user.role == 'Healthcare Provider':
        return redirect('provider_dashboard')
    elif request.user.role == 'Admin':
        return redirect('admin_dashboard')


#----------------------------- patient dashboard functions -----------------------
# view and edit profile info
# @login_required
# def patient_profile(request):
#     user = request.user

#     if request.method == "POST":
#         # update info
#         user.first_name = request.POST['first_name']
#         user.last_name = request.POST['last_name']
#         date_of_birth_str = request.POST['date_of_birth']
#         try:
#             date_of_birth = datetime.strptime(date_of_birth_str, '%d-%m-%Y').date()  # Parse the date
#             user.date_of_birth = date_of_birth
#         except ValueError:
#             messages.error(request, "Invalid date format. Please use DD-MM-YYYY.")
#             return render(request, 'CarePath/patient_profile.html', {'user': user})


#         user.email = request.POST['email']
#         user.phone_number = request.POST['phone_number']
#         user.address = request.POST['address']
#         user.save()

#         messages.success(request, "Your profile has been updated successfully!")
#         return redirect('patient_profile')  

#     return render(request, 'CarePath/patient_profile.html', {
#         'user': user,
#     })
@login_required
def patient_profile(request, id):
     # Get the patient based on the provided id
    patient = get_object_or_404(CustomUser, id=id, role='Patient')

    # If the current user is the patient, allow editing; otherwise, restrict to view only
    if request.user == patient:
        if request.method == "POST":
            # Update the patient's profile info
            patient.first_name = request.POST['first_name']
            patient.last_name = request.POST['last_name']

            # Parse the date of birth
            date_of_birth_str = request.POST['date_of_birth']
            try:
                date_of_birth = datetime.strptime(date_of_birth_str, '%d-%m-%Y').date()  # Parse the date
                patient.date_of_birth = date_of_birth
            except ValueError:
                messages.error(request, "Invalid date format. Please use DD-MM-YYYY.")
                return render(request, 'CarePath/patient_profile.html', {'user': patient, 'is_editable': True})

            patient.email = request.POST['email']
            patient.phone_number = request.POST['phone_number']
            patient.address = request.POST['address']
            patient.save()

            messages.success(request, "Your profile has been updated successfully!")
            return redirect('patient_profile', id=patient.id)

        return render(request, 'CarePath/patient_profile.html', {
            'user': patient,
            'is_editable': True
        })
    else:
        # If the logged-in user is not the patient, show the profile as read-only
        return render(request, 'CarePath/patient_profile.html', {
            'user': patient,
            'is_editable': False
        })






# change password
class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'CarePath/patient_password.html'
    success_url = reverse_lazy('patient_profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['password_help_texts'] = password_validators_help_texts()
        return context

    def form_invalid(self, form):
        # Check which fields caused validation errors
        for field in form.errors:
            if field == 'old_password':
                messages.error(self.request, _('The old password you entered is incorrect.'))
            elif field == 'new_password1' or field == 'new_password2':
                messages.error(self.request, _('The new passwords you entered do not match.'))
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, _('Your password has been updated successfully!'))
        return super().form_valid(form)
    

# display pt appointments
@login_required
def patient_appt(request):
    return render(request, 'CarePath/patient_appt.html')





#----------------------------- healthcare provider dashboard functions -----------------------
# view and edit profile info
@login_required
def provider_profile(request):
    user = request.user

    if request.method == "POST":
        # update info
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.phone_number = request.POST['phone_number']
        user.department = request.POST['department']
        user.provider_role = request.POST['provider_role']
        user.save()

        messages.success(request, "Your profile has been updated successfully!")
        return redirect('provider_profile')  

    return render(request, 'CarePath/provider_profile.html', {
        'user': user,
    })



# change password
class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'CarePath/provider_password.html'
    success_url = reverse_lazy('provider_profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['password_help_texts'] = password_validators_help_texts()
        return context

    def form_invalid(self, form):
        # Check which fields caused validation errors
        for field in form.errors:
            if field == 'old_password':
                messages.error(self.request, _('The old password you entered is incorrect.'))
            elif field == 'new_password1' or field == 'new_password2':
                messages.error(self.request, _('The new passwords you entered do not match.'))
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, _('Your password has been updated successfully!'))
        return super().form_valid(form)
    

# display healthcare provider appointments
# @login_required
# def provider_appt(request):
#     return render(request, 'CarePath/provider_appt.html')

# display healthcare provider appointments
@login_required
def provider_appt(request):
    # Get all appointments where the provider is the logged-in user, sorted by date and time
    appointments = Appointment.objects.filter(provider=request.user).order_by('date', 'start_time')

    # Calculate duration and pass it along with the appointments to the template
    appointment_data = []
    for appt in appointments:
        # Combine date and time to create datetime objects
        start_datetime = datetime.combine(appt.date, appt.start_time)
        finish_datetime = datetime.combine(appt.date, appt.finish_time)
        duration = finish_datetime - start_datetime  # Calculate the duration as timedelta

        # Convert duration to minutes
        duration_in_minutes = duration.total_seconds() / 60

        appointment_data.append({
            'date': appt.date,
            'start_time': appt.start_time,
            'finish_time': appt.finish_time,
            'duration': duration_in_minutes,
            'location': appt.location,
            'notes': appt.notes,
            'patient_name': f"{appt.patient.first_name} {appt.patient.last_name}",
            'patient_id': appt.patient.id,
            'appointment_id': appt.id
        })

    return render(request, 'CarePath/provider_appt.html', {
        'appointment_data': appointment_data
    })



#  view more appt info
@login_required
def view_more_appt_info(request, patient_id, appointment_id):
    # Get patient and appointment details
    patient = get_object_or_404(CustomUser, id=patient_id, role='Patient')
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=patient)

    # Combine date and time to create datetime objects
    start_datetime = datetime.combine(appointment.date, appointment.start_time)
    finish_datetime = datetime.combine(appointment.date, appointment.finish_time)
    
    # Calculate the duration in minutes
    duration = finish_datetime - start_datetime
    duration_in_minutes = duration.total_seconds() / 60

    return render(request, 'CarePath/view_more_appt_info.html', {
        'patient': patient,
        'appointment': appointment,
        'duration_in_minutes': duration_in_minutes
    })



# search pt
@login_required
def provider_search_pt(request):
    query = request.GET.get('q')  
    patients = None

    if query:
        patients = CustomUser.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query),
            role='Patient'
        )

    context = {
        'patients': patients
    }

    return render(request, 'CarePath/provider_search_pt.html', context)

# view pt profile
# @login_required
# def provider_view_pt(request, id):
#     patient = get_object_or_404(CustomUser, id=id, role='Patient')
#     return render(request, 'CarePath/patient_profile.html', {'user': patient, 'is_editable': False})
@login_required
def provider_view_pt(request, id):
    # Get the patient by ID
    patient = get_object_or_404(CustomUser, id=id, role='Patient')
    
    # Render the template with both the provider (user) and the patient
    return render(request, 'CarePath/patient_profile.html', {
        'user': request.user,  # The healthcare provider
        'patient': patient,    # The patient being viewed
        'is_editable': False   # No editing allowed for the provider
    })


# choose a patient to book appt
@login_required
def book_pt_appointment(request, patient_id):
    patient = get_object_or_404(CustomUser, id=patient_id, role='Patient')

     # Get all healthcare providers to populate the dropdown list
    providers = CustomUser.objects.filter(role='Healthcare Provider')

    if request.method == "POST":
        date = request.POST['date']
        start_time = request.POST['start_time']
        finish_time = request.POST['finish_time']
        location = request.POST['location']
        provider_id = request.POST['provider']  # Get selected provider ID
        notes = request.POST.get('notes', '')  # Optional field

        provider = CustomUser.objects.get(id=provider_id)

        # Validate that start_time < finish_time
        if time.fromisoformat(start_time) >= time.fromisoformat(finish_time):
            messages.error(request, "Start time must be earlier than finish time.")
            return render(request, 'CarePath/book_pt_appointment.html', {'patient': patient})


         # Check if the patient already has an appointment at the chosen time
        patient_conflict = Appointment.objects.filter(
            patient=patient,
            date=date,
            start_time__lt=finish_time,
            finish_time__gt=start_time
        ).exists()

        # Check if the provider already has an appointment at the chosen time
        provider_conflict = Appointment.objects.filter(
            provider=provider,
            date=date,
            start_time__lt=finish_time,
            finish_time__gt=start_time
        ).exists()

        if patient_conflict or provider_conflict:
            messages.error(request, "The patient or provider already has an appointment at the chosen time.")
            return render(request, 'CarePath/book_pt_appointment.html', {'patient': patient, 'providers': providers})


        # Create a new appointment if there are no conflicts
        appointment = Appointment.objects.create(
            patient=patient,
            provider=provider,
            date=date,
            start_time=start_time,
            finish_time=finish_time,
            location=location,
            notes=notes
        )
        appointment.save()

        messages.success(request, "Appointment successfully booked for {}.".format(patient.first_name))
        # return redirect('provider_view_pt', id=patient.id)
        return redirect('provider_appt')

    return render(request, 'CarePath/book_pt_appointment.html', {'patient': patient, 'providers': providers })
