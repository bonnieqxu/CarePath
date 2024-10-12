
import os
from datetime import date, time, datetime,  timedelta

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.messages import get_messages
from django.contrib.auth import get_user_model, authenticate, login as auth_login
from django.contrib.auth.password_validation import password_validators_help_texts
from django.contrib.auth.models import Group
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.sites.shortcuts import get_current_site

from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.timezone import datetime
from django.utils.translation import gettext as _


from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404

from django.db.models import Q
from django.template.loader import render_to_string

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail




from .models import CustomUser, Appointment, Message, Feedback


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



# create an account
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
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            password=password,
            role=role,
            is_active=False  # User account is inactive until email is verified
        )

        # Set additional fields for patients
        if role == 'Patient':
            if date_of_birth:  
                user.date_of_birth = date_of_birth
            if address:
                user.address = address

        if role == 'Healthcare Provider':
            if department:
                user.department = department
            if provider_role:
                user.provider_role = provider_role
            user.status = 'Disabled'  # Provider will still need admin approval after email activation

        user.save()
        
        # Assign the user to the appropriate group based on the role
        group = Group.objects.get(name=role)
        user.groups.add(group)

        # Send activation email
        send_activation_email(request, user)

        # Inform the user that the activation email has been sent
        return render(request, 'CarePath/activation_sent.html')

    return render(request, 'CarePath/register.html', {'today_date': today_date})



# def check_email_availability(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         available = not CustomUser.objects.filter(email=email).exists()
#         return JsonResponse({'available': available})
    
def check_email_availability(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            available = not CustomUser.objects.filter(email=email).exists()
            return JsonResponse({'available': available})
        else:
            return JsonResponse({'error': 'Invalid email input'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

# Helper function to send activation email using SendGrid
def send_activation_email(request, user):
    current_site = get_current_site(request)
    mail_subject = 'Activate your CarePath account'
    
    # Encoding user ID and generating token
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = token_generator.make_token(user)
    
    # Generating activation link
    activation_link = reverse('activate_user', kwargs={'uidb64': uidb64, 'token': token})
    activation_url = f'http://{current_site.domain}{activation_link}'
    
    
    # Render the email content using the template
    email_content = render_to_string('CarePath/activation_email.html', {
        'user': user,
        'activation_url': activation_url,
    })

    
    # Sending email with SendGrid
    email_message = Mail(
        from_email='bonnieoht@gmail.com',  
        to_emails=user.email,  # User's email
        subject=mail_subject,
        
        # html_content=f'<p>Hi {user.first_name},</p><p>Please click the following link to activate your account: <a href="{activation_url}">Activate Account</a></p>'
        html_content=email_content
    )

    

    try:
        # Retrieve the SendGrid API key securely from environment variable
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(email_message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(f'Error sending email: {str(e)}')



# handle email activation
def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        user.is_active = True  # Activate the account but wait for user confirmation
        user.save()

        # Navigate to the activate_account.html page for the user to confirm activation
        return render(request, 'CarePath/activate_account.html', {'user': user})

    else:
        return render(request, 'CarePath/activation_invalid.html')  # Handle invalid token or user


# handle account activation after user confirms
def confirm_account_activation(request, user_id):
    try:
        user = CustomUser.objects.get(pk=user_id)
    except CustomUser.DoesNotExist:
        return render(request, 'CarePath/activation_invalid.html')  # Handle invalid user

    # Add success message after activation
    messages.success(request, 'Your account is activated successfully!')

    # Redirect based on the user role
    if user.role == 'Healthcare Provider':
        return render(request, 'CarePath/account_pending.html')  # Navigate to account pending
    else:
        return redirect('login')  # For patients, navigate to login

# ---------------------------- VISITOR related views ends -----------------------







# --------------------------------- REGISTERED USER VIEWS ------------------------

# user login
def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)

        if user is not None:
            
            if user.role == 'Healthcare Provider':
                if not user.is_active:

                    messages.error(request, 'Your account has been disabled. Please contact the admin.')
                    return redirect('login')
                elif user.status == 'Disabled':
                    messages.info(request, 'Your account is pending admin approval.')
                    return render(request, 'CarePath/account_pending.html')

           
            auth_login(request, user)

            # Set success message
            messages.success(request, 'Your account is activated successfully!')

            if user.role == 'Patient':
                return redirect('patient_dashboard')
            elif user.role == 'Healthcare Provider' and user.status == 'Active':
                return redirect('provider_dashboard')
            elif user.role == 'Admin':
                return redirect('admin_dashboard')
        else:
           
            messages.error(request, 'Invalid email or password.')
            return redirect('login')
        
    return render(request, "CarePath/login.html")




# dashboards

@login_required
def patient_dashboard(request):
    patient = request.user  
    context = {
        'is_discharged': patient.status == 'Discharged'
    }
    return render(request, 'CarePath/patient_dashboard.html', context)


@login_required
def provider_dashboard(request):
    
    if request.user.role == 'Healthcare Provider' and request.user.status != 'Active':
        return render(request, 'CarePath/account_pending.html')  
    
    unread_feedback_count = Feedback.objects.filter(provider=request.user, is_read=False).count()

    context = {
        'unread_feedback_count': unread_feedback_count
    }

    return render(request, 'CarePath/provider_dashboard.html', context)


@login_required
def admin_dashboard(request):

    if request.user.role == 'Admin' and (not request.user.first_name or not request.user.last_name):
        messages.warning(request, 'Please complete your profile information.')
        return redirect('admin_profile')  


    pending_users = CustomUser.objects.filter(role='Healthcare Provider', status='Disabled')

    pending_users_count = pending_users.count()

    context = {
        'pending_users_count': pending_users_count,
    }

    return render(request, 'CarePath/admin_dashboard.html', context)



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
# def patient_profile(request, id):
#      # Get the patient based on the provided id
#     patient = get_object_or_404(CustomUser, id=id, role='Patient')

#     # If the current user is the patient, allow editing; otherwise, restrict to view only
#     if request.user == patient:
#         if request.method == "POST":
#             # Update the patient's profile info
#             patient.first_name = request.POST['first_name']
#             patient.last_name = request.POST['last_name']

#             # Parse the date of birth
#             date_of_birth_str = request.POST['date_of_birth']
#             try:
#                 date_of_birth = datetime.strptime(date_of_birth_str, '%d-%m-%Y').date()  # Parse the date
#                 patient.date_of_birth = date_of_birth
#             except ValueError:
#                 messages.error(request, "Invalid date format. Please use DD-MM-YYYY.")
#                 return render(request, 'CarePath/patient_profile.html', {'user': patient, 'is_editable': True})

#             patient.email = request.POST['email']
#             patient.phone_number = request.POST['phone_number']
#             patient.address = request.POST['address']
#             patient.save()

#             messages.success(request, "Your profile has been updated successfully!")
#             return redirect('patient_profile', id=patient.id)

#         return render(request, 'CarePath/patient_profile.html', {
#             'user': patient,
#             'is_editable': True
#         })
#     else:
#         # If the logged-in user is not the patient, show the profile as read-only
#         return render(request, 'CarePath/patient_profile.html', {
#             'user': patient,
#             'is_editable': False
#         })


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

            # Parse and validate the date of birth
            date_of_birth_str = request.POST['date_of_birth']
            try:
                date_of_birth = datetime.strptime(date_of_birth_str, '%d-%m-%Y').date()  # Parse the date
                if date_of_birth > date.today():
                    messages.error(request, "Date of birth cannot be in the future.")
                    return render(request, 'CarePath/patient_profile.html', {'user': patient, 'is_editable': True})
                patient.date_of_birth = date_of_birth
            except ValueError:
                messages.error(request, "Invalid date format. Please use DD-MM-YYYY.")
                return render(request, 'CarePath/patient_profile.html', {'user': patient, 'is_editable': True})

            patient.phone_number = request.POST['phone_number']
            patient.address = request.POST['address']


            patient.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('patient_profile', id=patient.id)

        today_date = date.today().strftime('%d-%m-%Y')
        return render(request, 'CarePath/patient_profile.html', {
            'user': patient,
            'is_editable': True,
            'today_date': today_date
        })
    else:
        # If the logged-in user is not the patient, show the profile as read-only
        return render(request, 'CarePath/patient_profile.html', {
            'user': patient,
            'is_editable': False
        })





# change password
# class PatientPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
#     template_name = 'CarePath/patient_password.html'
#     success_url = reverse_lazy('patient_profile')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['password_help_texts'] = password_validators_help_texts()
#         return context

#     def form_invalid(self, form):
#         # Check which fields caused validation errors
#         for field in form.errors:
#             if field == 'old_password':
#                 messages.error(self.request, _('The old password you entered is incorrect.'))
#             elif field == 'new_password1' or field == 'new_password2':
#                 messages.error(self.request, _('The new passwords you entered do not match.'))
#         return super().form_invalid(form)

#     def form_valid(self, form):
#         messages.success(self.request, _('Your password has been updated successfully!'))
#         return super().form_valid(form)
    



class PatientPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'CarePath/patient_password.html'

    def get_success_url(self):
        # Return the URL for the patient's profile page with the user ID
        return reverse('patient_profile', kwargs={'id': self.request.user.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['password_help_texts'] = password_validators_help_texts()
        return context

    def form_invalid(self, form):
        # Check which fields caused validation errors
        for field in form.errors:
            if field == 'old_password':
                messages.error(self.request, _('The old password you entered is incorrect.'))
            elif field in ['new_password1', 'new_password2']:
                messages.error(self.request, _('The new passwords you entered do not match.'))
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, _('Your password has been updated successfully!'))
        return super().form_valid(form)


# display pt appointments
from datetime import datetime

@login_required
def patient_appt(request):
    # Get today's date
    today = datetime.now().date()

    # Get all future appointments where the patient is the logged-in user, sorted by date and time
    appointments = Appointment.objects.filter(patient=request.user, date__gte=today).order_by('date', 'start_time')

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
            'provider_name': f"{appt.provider.first_name} {appt.provider.last_name}",
            'provider': appt.provider,  
            'patient_id': appt.patient.id,
            'appointment_id': appt.id
        })

    return render(request, 'CarePath/patient_appt.html', {
        'appointment_data': appointment_data
    })

# @login_required
# def patient_appt(request):
#     # Get all appointments where the patient is the logged-in user, sorted by date and time
#     appointments = Appointment.objects.filter(patient=request.user).order_by('date', 'start_time')

#     # Calculate duration and pass it along with the appointments to the template
#     appointment_data = []
#     for appt in appointments:
#         # Combine date and time to create datetime objects
#         start_datetime = datetime.combine(appt.date, appt.start_time)
#         finish_datetime = datetime.combine(appt.date, appt.finish_time)
#         duration = finish_datetime - start_datetime  # Calculate the duration as timedelta

#         # Convert duration to minutes
#         duration_in_minutes = duration.total_seconds() / 60

#         appointment_data.append({
#             'date': appt.date,
#             'start_time': appt.start_time,
#             'finish_time': appt.finish_time,
#             'duration': duration_in_minutes,
#             'location': appt.location,
#             'notes': appt.notes,
#             'patient_name': f"{appt.patient.first_name} {appt.patient.last_name}",
#             'provider_name': f"{appt.provider.first_name} {appt.provider.last_name}",
#             'provider': appt.provider,  
#             'patient_id': appt.patient.id,
#             'appointment_id': appt.id
#         })


#     return render(request, 'CarePath/patient_appt.html', {
#         'appointment_data': appointment_data
#     })

# pt view their healthcare provider details
@login_required
def view_provider_details(request, provider_id):
    provider = get_object_or_404(CustomUser, id=provider_id)
    print(f"Provider ID: {provider.id}, Name: {provider.first_name} {provider.last_name}, Role: {provider.role}")
    return render(request, 'CarePath/view_provider_details.html', {
        'provider': provider
    })





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
class ProviderPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
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
@login_required
def provider_appt(request):
    # Get today's date
    today = datetime.now().date()

    # Get all future appointments where the provider is the logged-in user, sorted by date and time
    appointments = Appointment.objects.filter(provider=request.user, date__gte=today).order_by('date', 'start_time')

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

# @login_required
# def provider_appt(request):
#     # Get all appointments where the provider is the logged-in user, sorted by date and time
#     appointments = Appointment.objects.filter(provider=request.user).order_by('date', 'start_time')

#     # Calculate duration and pass it along with the appointments to the template
#     appointment_data = []
#     for appt in appointments:
#         # Combine date and time to create datetime objects
#         start_datetime = datetime.combine(appt.date, appt.start_time)
#         finish_datetime = datetime.combine(appt.date, appt.finish_time)
#         duration = finish_datetime - start_datetime  # Calculate the duration as timedelta

#         # Convert duration to minutes
#         duration_in_minutes = duration.total_seconds() / 60

#         appointment_data.append({
#             'date': appt.date,
#             'start_time': appt.start_time,
#             'finish_time': appt.finish_time,
#             'duration': duration_in_minutes,
#             'location': appt.location,
#             'notes': appt.notes,
#             'patient_name': f"{appt.patient.first_name} {appt.patient.last_name}",
#             'patient_id': appt.patient.id,
#             'appointment_id': appt.id
#         })

#     return render(request, 'CarePath/provider_appt.html', {
#         'appointment_data': appointment_data
#     })




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

@login_required
def view_patient_details(request, id):
    patient = get_object_or_404(CustomUser, id=id, role='Patient')
    return render(request, 'CarePath/view_patient_details.html', {'patient': patient})


# book an appt for the chosen pt
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


        # Convert the date string to a datetime object
        try:
            appointment_date = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Invalid date format.")
            return render(request, 'CarePath/book_pt_appointment.html', {'patient': patient, 'providers': providers})

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


        formatted_date = appointment_date.strftime('%d-%m-%Y')

        # Send a message to the patient
        Message.objects.create(
            recipient=patient,
            content=f"Your appointment on {formatted_date} at {appointment.start_time} with Dr {provider.first_name} {provider.last_name} has been successfully booked."
        )


        messages.success(request, "Appointment successfully booked for {}. A message has been sent to the patient.".format(patient.first_name))
        # return redirect('provider_view_pt', id=patient.id)
        return redirect('provider_appt')

    return render(request, 'CarePath/book_pt_appointment.html', {'patient': patient, 'providers': providers })



# cancel appt
@login_required
def cancel_appt(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    patient = appointment.patient

    appointment.delete()

     # Format the date to 'dd-mm-yyyy'
    formatted_date = appointment.date.strftime('%d-%m-%Y')


    # Send a message to the patient
    Message.objects.create(
        recipient=patient,
        content=f"Your appointment on {formatted_date} at {appointment.start_time} has been cancelled."
    )

    messages.success(request, "The appointment has been successfully cancelled. A message has been sent to the patient.")

    return redirect(reverse('provider_appt'))


# edit an appt
@login_required
def edit_appt(request, patient_id, appointment_id):
    # Get patient and appointment details
    patient = get_object_or_404(CustomUser, id=patient_id, role='Patient')
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=patient)

    if request.method == "POST":
        location = request.POST['location']
        notes = request.POST.get('notes', '')

        # Convert the date and time from the form into datetime objects
        try:
            appointment_date = datetime.strptime(request.POST['date'], '%Y-%m-%d').date()
            start_time = datetime.strptime(request.POST['start_time'], '%H:%M').time()
            finish_time = datetime.strptime(request.POST['finish_time'], '%H:%M').time()
        except ValueError:
            messages.error(request, "Invalid date or time format.")
            return render(request, 'CarePath/edit_appt.html', {'patient': patient, 'appointment': appointment})

        # Validation: Date must be a weekday (Mon-Fri)
        if appointment_date.weekday() >= 5:  # 5 is Saturday, 6 is Sunday
            messages.error(request, "Appointments can only be scheduled on weekdays (Mon-Fri).")
            return render(request, 'CarePath/edit_appt.html', {'patient': patient, 'appointment': appointment})

        # Validation: Start time cannot be earlier than 8am, finish time cannot be later than 4:30pm
        earliest_start_time = time(8, 0)  # 8:00 AM
        latest_finish_time = time(16, 30)  # 4:30 PM

        if start_time < earliest_start_time:
            messages.error(request, "Start time cannot be earlier than 8:00 AM.")
            return render(request, 'CarePath/edit_appt.html', {'patient': patient, 'appointment': appointment})

        if finish_time > latest_finish_time:
            messages.error(request, "Finish time cannot be later than 4:30 PM.")
            return render(request, 'CarePath/edit_appt.html', {'patient': patient, 'appointment': appointment})

        # Validation: Finish time must be later than start time
        if start_time >= finish_time:
            messages.error(request, "Finish time must be later than start time.")
            return render(request, 'CarePath/edit_appt.html', {'patient': patient, 'appointment': appointment})

        # Check if the patient has another appointment during the same time
        patient_conflict = Appointment.objects.filter(
            patient=patient,
            date=appointment_date,
            start_time__lt=finish_time,
            finish_time__gt=start_time
        ).exclude(id=appointment_id)  # Exclude current appointment

        # Check if the provider has another appointment during the same time
        provider_conflict = Appointment.objects.filter(
            provider=appointment.provider,
            date=appointment_date,
            start_time__lt=finish_time,
            finish_time__gt=start_time
        ).exclude(id=appointment_id)  # Exclude current appointment

        if patient_conflict.exists() or provider_conflict.exists():
            messages.error(request, "The patient or provider already has an appointment at the chosen time.")
            return render(request, 'CarePath/edit_appt.html', {'patient': patient, 'appointment': appointment})

        # If no conflicts, update the appointment with new values
        appointment.date = appointment_date
        appointment.start_time = start_time
        appointment.finish_time = finish_time
        appointment.location = location
        appointment.notes = notes
        appointment.save()

        formatted_date = appointment.date.strftime('%d-%m-%Y')

         # Send message to the patient
        Message.objects.create(
            recipient=patient,
            content=f"Your appointment on {formatted_date} has been updated. Please check the updated information."
        )

        messages.success(request, "Appointment updated successfully!")

        # Send a success message to the patient
        messages.success(request, f"A message has been sent to {patient.first_name}.")

        return redirect('provider_appt')

    # Pre-load current appointment data for the form
    return render(request, 'CarePath/edit_appt.html', {
        'patient': patient,
        'appointment': appointment
    })


#  ------------------------ communication functions --------------------------


@login_required
def patient_communication(request):
    # Fetch patient's messages
    messages = Message.objects.filter(recipient=request.user).order_by('-created_at')

    # Fetch patient's reminders (appointments in the next 3 days)
    today = date.today()
    reminders = Appointment.objects.filter(
        patient=request.user,
        date__range=[today, today + timedelta(days=3)]
    )

    # Count unread messages
    unread_messages_count = Message.objects.filter(recipient=request.user, is_read=False).count()

    # Since reminders are not marked as read/unread, use the number of reminders as the count
    # unread_reminders_count = reminders.count()

    unread_reminders_count = Appointment.objects.filter(patient=request.user, is_read=False, date__range=[today, today + timedelta(days=3)]).count()

    # Get the list of providers for feedback
    providers = CustomUser.objects.filter(role__in=['Healthcare Provider', 'Admin'])

    return render(request, 'CarePath/patient_communication.html', {
        'messages': messages,
        'reminders': reminders,
        'providers': providers,
        'unread_messages_count': unread_messages_count,
        'unread_reminders_count': unread_reminders_count
    })




def update_recipients_view(request):
    for message in Message.objects.all():
        message.recipient = message.user  # Assuming 'user' field stores the correct user
        message.save()

    return HttpResponse('Recipient fields updated successfully')




@login_required
def patient_messages(request):
    # Get messages for the logged-in patient
    messages = Message.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'CarePath/patient_messages.html', {'messages': messages})




@login_required
def mark_as_read(request, message_id):
    try:
        message = Message.objects.get(id=message_id, recipient=request.user)
        message.is_read = True
        message.save()
        messages.success(request, "Message marked as read.")
    except Message.DoesNotExist:
        messages.error(request, "Message not found.")
    return redirect('patient_communication')


@login_required
def mark_as_unread(request, message_id):
    try:
        message = Message.objects.get(id=message_id, recipient=request.user)
        message.is_read = False
        message.save()
        messages.success(request, "Message marked as unread.")
    except Message.DoesNotExist:
        messages.error(request, "Message not found.")
    return redirect('patient_communication')


@login_required
def delete_message(request, message_id):
    try:
        message = Message.objects.get(id=message_id, recipient=request.user)
        message.delete()
        messages.success(request, "Message deleted successfully.")
    except Message.DoesNotExist:
        messages.error(request, "Message not found.")
    return redirect('patient_communication')



@login_required
def patient_reminders(request):
    # Get reminders for upcoming appointments in the next 3 days
    today = date.today()
    reminders = Appointment.objects.filter(
        patient=request.user,
        date__range=[today, today + timedelta(days=3)]
    )
    return render(request, 'CarePath/patient_reminders.html', {'reminders': reminders})

@login_required
def mark_reminder_as_read(request, reminder_id):
    reminder = get_object_or_404(Appointment, id=reminder_id, patient=request.user)
    reminder.is_read = True
    reminder.save()
    messages.success(request, 'Reminder marked as read.')
    return redirect('patient_communication')

@login_required
def mark_reminder_as_unread(request, reminder_id):
    reminder = get_object_or_404(Appointment, id=reminder_id, patient=request.user)
    reminder.is_read = False
    reminder.save()
    messages.success(request, 'Reminder marked as unread.')
    return redirect('patient_communication')

@login_required
def delete_reminder(request, reminder_id):
    reminder = get_object_or_404(Appointment, id=reminder_id, patient=request.user)
    reminder.delete()
    messages.success(request, 'Reminder deleted.')
    return redirect('patient_communication')


@login_required
def patient_feedback(request):
    if request.method == 'POST':
        feedback_text = request.POST.get('feedback')
        provider_id = request.POST.get('provider_id')
        provider = get_object_or_404(CustomUser, id=provider_id, role__in=['Healthcare Provider', 'Admin'])
        
        # Save feedback
        Feedback.objects.create(
            patient=request.user,
            provider=provider,
            feedback=feedback_text,
        )
        messages.success(request, 'Feedback sent successfully.')
        return redirect('patient_feedback')

    # Get healthcare providers and admins to allow selection
    providers = CustomUser.objects.filter(role__in=['Healthcare Provider', 'Admin'])
    return render(request, 'CarePath/patient_feedback.html', {'providers': providers})



# @login_required
# def submit_feedback(request):
#     if request.method == "POST":
#         provider_id = request.POST['provider']
#         feedback_content = request.POST['feedback']
#         provider = CustomUser.objects.get(id=provider_id)
        
#         Feedback.objects.create(
#             patient=request.user,
#             provider=provider,
#             feedback=feedback_content,
#         )
#         messages.success(request, 'Your feedback has been submitted successfully!', extra_tags='feedback_success')
    

#     return HttpResponseRedirect(reverse('patient_communication') + '#feedback')


@login_required
def submit_feedback(request):
    if request.method == "POST":
        provider_id = request.POST['provider']
        feedback_content = request.POST['feedback']
        provider = CustomUser.objects.get(id=provider_id)
        
        # Create feedback entry in the database
        Feedback.objects.create(
            patient=request.user,
            provider=provider,
            feedback=feedback_content,
        )

        # Clear any existing messages
        storage = get_messages(request)
        for _ in storage:
            pass  # This will clear the messages queue

        # Add only the feedback submission success message
        messages.success(request, 'Your feedback has been submitted successfully!', extra_tags='feedback_success')
    
    return HttpResponseRedirect(reverse('patient_communication') + '#feedback')


# healthcare providers

@login_required
def provider_feedback(request):
    
    # Get feedback directed at the healthcare provider
    feedbacks = Feedback.objects.filter(provider=request.user).order_by('-created_at')

    unread_feedback_count = Feedback.objects.filter(provider=request.user, is_read=False).count()
    
    context = {
        'feedbacks': feedbacks,
        'unread_feedback_count': unread_feedback_count  
    }

    return render(request, 'CarePath/provider_feedback.html', context)



@login_required
def mark_feedback_as_read(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    feedback.is_read = True
    feedback.save()
    messages.success(request, 'Feedback marked as read.')
    return redirect('provider_feedback')

@login_required
def mark_feedback_as_unread(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    feedback.is_read = False
    feedback.save()
    messages.success(request, 'Feedback marked as unread.')
    return redirect('provider_feedback')

@login_required
def delete_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    feedback.delete()
    messages.success(request, 'Feedback has been deleted.')
    return redirect('provider_feedback')




# ADMIN


# @login_required
# def admin_feedback(request):
#     # Ensure only admins can access this view
#     if not request.user.is_staff:  # Assuming `is_staff` is used for admin users
#         return redirect('home')

#     # Get all feedback entries, sorted by date (newest first)
#     feedbacks = Feedback.objects.all().order_by('-created_at')

#     unread_feedback_count = Feedback.objects.filter(is_read=False).count()
    
#     context = {
#         'feedbacks': feedbacks,
#         'unread_feedback_count': unread_feedback_count
#     }

#     return render(request, 'CarePath/admin_feedback.html', context)

@login_required
def admin_feedback(request):
    # Ensure only admins can access this view
    if not request.user.is_staff:  # Assuming `is_staff` is used for admin users
        return redirect('home')

    # Get feedback directed at the admin user only
    feedbacks = Feedback.objects.filter(provider=request.user).order_by('-created_at')

    unread_feedback_count = Feedback.objects.filter(provider=request.user, is_read=False).count()
    
    context = {
        'feedbacks': feedbacks,
        'unread_feedback_count': unread_feedback_count
    }

    return render(request, 'CarePath/admin_feedback.html', context)


@login_required
def mark_admin_feedback_as_read(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    feedback.is_read = True
    feedback.save()
    messages.success(request, 'Feedback marked as read.')
    return redirect('admin_feedback')

@login_required
def mark_admin_feedback_as_unread(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    feedback.is_read = False
    feedback.save()
    messages.success(request, 'Feedback marked as unread.')
    return redirect('admin_feedback')

@login_required
def delete_admin_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    feedback.delete()
    messages.success(request, 'Feedback has been deleted.')
    return redirect('admin_feedback')



# ------------------------------ admin functions -------------------------------

# view and edit profile info
@login_required
def admin_profile(request):
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
        return redirect('admin_profile')  

    return render(request, 'CarePath/admin_profile.html', {
        'user': user,
    })

# change password
class AdminPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'CarePath/admin_password.html'
    success_url = reverse_lazy('admin_profile')

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
    



# view all appts

@login_required
def all_appointments(request):
    # Get today's date to filter future appointments
    today = timezone.now().date()

    # Retrieve appointments starting from today and beyond
    appointments = Appointment.objects.filter(date__gte=today)

    date_filter = request.GET.get('date', None)
    provider_id = request.GET.get('provider', None)
    patient_id = request.GET.get('patient', None)
    location = request.GET.get('location', None)

    # Apply filters based on the user's selections
    if date_filter:
        appointments = appointments.filter(date=date_filter)
    if provider_id:
        appointments = appointments.filter(provider__id=provider_id)
    if patient_id:
        appointments = appointments.filter(patient__id=patient_id)
    if location:
        appointments = appointments.filter(location__icontains=location)

    # Order the filtered appointments by date and start time
    appointments = appointments.order_by('date', 'start_time')

    # Retrieve lists of healthcare providers and patients for the filter options
    providers = CustomUser.objects.filter(role='Healthcare Provider')
    patients = CustomUser.objects.filter(role='Patient')

    today_date = date.today().strftime('%Y-%m-%d')

    # Pass the filtered appointments, today_date, and other data to the template
    context = {
        'appointments': appointments,
        'providers': providers,
        'patients': patients,
        'selected_date': date_filter,
        'selected_provider': provider_id,
        'selected_patient': patient_id,
        'selected_location': location,
        'today_date': today_date,  # Pass today's date to the template for date restriction
    }

    return render(request, 'CarePath/all_appointments.html', context)

# @login_required
# def all_appointments(request):
#     appointments = Appointment.objects.all()

#     # Fetch filter values from the request
#     date_filter = request.GET.get('date', None)
#     provider_id = request.GET.get('provider', None)
#     patient_id = request.GET.get('patient', None)
#     location = request.GET.get('location', None)

#     # Apply filters to the appointments queryset
#     if date_filter:
#         appointments = appointments.filter(date=date_filter)
#     if provider_id:
#         appointments = appointments.filter(provider__id=provider_id)
#     if patient_id:
#         appointments = appointments.filter(patient__id=patient_id)
#     if location:
#         appointments = appointments.filter(location__icontains=location)

#     # Order the appointments by date and time
#     appointments = appointments.order_by('date', 'start_time')

#     # Get the list of providers and patients
#     providers = CustomUser.objects.filter(role='Healthcare Provider')
#     patients = CustomUser.objects.filter(role='Patient')

#     # Add today's date to the context to set the minimum value for the date picker
#     today_date = date.today().strftime('%Y-%m-%d')

#     context = {
#         'appointments': appointments,
#         'providers': providers,
#         'patients': patients,
#         'selected_date': date_filter,
#         'selected_provider': provider_id,
#         'selected_patient': patient_id,
#         'selected_location': location,
#         'today_date': today_date,  # Pass today's date to the template
#     }

#     return render(request, 'CarePath/all_appointments.html', context)

# @login_required
# def all_appointments(request):
#     appointments = Appointment.objects.all()

#     date = request.GET.get('date', None)
#     provider_id = request.GET.get('provider', None)
#     patient_id = request.GET.get('patient', None)
#     location = request.GET.get('location', None)

#     if date:
#         appointments = appointments.filter(date=date)
#     if provider_id:
#         appointments = appointments.filter(provider__id=provider_id)
#     if patient_id:
#         appointments = appointments.filter(patient__id=patient_id)
#     if location:
#         appointments = appointments.filter(location__icontains=location)

#     appointments = appointments.order_by('date', 'start_time')
    
#     providers = CustomUser.objects.filter(role='Healthcare Provider')
#     patients = CustomUser.objects.filter(role='Patient')

#     context = {
#         'appointments': appointments,
#         'providers': providers,
#         'patients': patients,
#         'selected_date': date,
#         'selected_provider': provider_id,
#         'selected_patient': patient_id,
#         'selected_location': location,
#     }

#     return render(request, 'CarePath/all_appointments.html', context)


# search pt
@login_required
def admin_search_pt(request):
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

    return render(request, 'CarePath/admin_search_pt.html', context)

# view pt into
@login_required
def admin_view_pt(request, id):
    # Get the patient by ID
    patient = get_object_or_404(CustomUser, id=id, role='Patient')
    
    # Render the template with both the admin (user) and the patient
    return render(request, 'CarePath/admin_patient_profile.html', {
        'user': request.user,  # The admin
        'patient': patient,    # The patient being viewed
        'is_editable': False   # No editing allowed for the admin
    })

# add a new booking
@login_required
def admin_book_pt_appointment(request, patient_id):
    patient = get_object_or_404(CustomUser, id=patient_id, role='Patient')
    providers = CustomUser.objects.filter(role='Healthcare Provider')

    if request.method == "POST":
        date = request.POST['date']
        start_time = request.POST['start_time']
        finish_time = request.POST['finish_time']
        location = request.POST['location']
        provider_id = request.POST['provider']  
        notes = request.POST.get('notes', '')

        provider = CustomUser.objects.get(id=provider_id)

        try:
            appointment_date = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Invalid date format.")
            return render(request, 'CarePath/admin_book_pt_appointment.html', {'patient': patient, 'providers': providers})

        if time.fromisoformat(start_time) >= time.fromisoformat(finish_time):
            messages.error(request, "Start time must be earlier than finish time.")
            return render(request, 'CarePath/admin_book_pt_appointment.html', {'patient': patient})

        # Check conflicts
        patient_conflict = Appointment.objects.filter(
            patient=patient,
            date=date,
            start_time__lt=finish_time,
            finish_time__gt=start_time
        ).exists()

        provider_conflict = Appointment.objects.filter(
            provider=provider,
            date=date,
            start_time__lt=finish_time,
            finish_time__gt=start_time
        ).exists()

        if patient_conflict or provider_conflict:
            messages.error(request, "The patient or provider already has an appointment at the chosen time.")
            return render(request, 'CarePath/admin_book_pt_appointment.html', {'patient': patient, 'providers': providers})

        # Create a new appointment
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

        formatted_date = appointment_date.strftime('%d-%m-%Y')
        Message.objects.create(
            recipient=patient,
            content=f"Your appointment on {formatted_date} at {appointment.start_time} with Dr {provider.first_name} {provider.last_name} has been successfully booked."
        )

        messages.success(request, "Appointment successfully booked for {}. A message has been sent to the patient.".format(patient.first_name))
        return redirect('all_appointments')

    return render(request, 'CarePath/admin_book_pt_appointment.html', {'patient': patient, 'providers': providers})

# cancel appt
@login_required
def admin_cancel_appt(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    patient = appointment.patient

    formatted_date = appointment.date.strftime('%d-%m-%Y')
    appointment.delete()

    Message.objects.create(
        recipient=patient,
        content=f"Your appointment on {formatted_date} at {appointment.start_time} has been cancelled."
    )

    messages.success(request, "The appointment has been successfully cancelled. A message has been sent to the patient.")
    return redirect('all_appointments')

# edit appt
@login_required
def admin_edit_appt(request, patient_id, appointment_id):
    patient = get_object_or_404(CustomUser, id=patient_id, role='Patient')
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=patient)

    if request.method == "POST":
        location = request.POST['location']
        notes = request.POST.get('notes', '')

        try:
            appointment_date = datetime.strptime(request.POST['date'], '%Y-%m-%d').date()
            start_time = datetime.strptime(request.POST['start_time'], '%H:%M').time()
            finish_time = datetime.strptime(request.POST['finish_time'], '%H:%M').time()
        except ValueError:
            messages.error(request, "Invalid date or time format.")
            return render(request, 'CarePath/admin_edit_appt.html', {'patient': patient, 'appointment': appointment})

        # Validations (same as provider)
        if appointment_date.weekday() >= 5 or start_time < time(8, 0) or finish_time > time(16, 30) or start_time >= finish_time:
            messages.error(request, "Invalid appointment time or date.")
            return render(request, 'CarePath/admin_edit_appt.html', {'patient': patient, 'appointment': appointment})

        patient_conflict = Appointment.objects.filter(
            patient=patient,
            date=appointment_date,
            start_time__lt=finish_time,
            finish_time__gt=start_time
        ).exclude(id=appointment_id)

        provider_conflict = Appointment.objects.filter(
            provider=appointment.provider,
            date=appointment_date,
            start_time__lt=finish_time,
            finish_time__gt=start_time
        ).exclude(id=appointment_id)

        if patient_conflict.exists() or provider_conflict.exists():
            messages.error(request, "Conflict with another appointment.")
            return render(request, 'CarePath/admin_edit_appt.html', {'patient': patient, 'appointment': appointment})

        # Save changes
        appointment.date = appointment_date
        appointment.start_time = start_time
        appointment.finish_time = finish_time
        appointment.location = location
        appointment.notes = notes
        appointment.save()

        formatted_date = appointment.date.strftime('%d-%m-%Y')
        Message.objects.create(
            recipient=patient,
            content=f"Your appointment on {formatted_date} has been updated. Please check the updated information."
        )

        messages.success(request, "Appointment updated successfully!")
        return redirect('all_appointments')

    return render(request, 'CarePath/admin_edit_appt.html', {
        'patient': patient,
        'appointment': appointment
    })


# admin manages users


@login_required
def manage_users(request):
    # get all users
    pending_users = CustomUser.objects.filter(role='Healthcare Provider', status='Disabled')
    active_users = CustomUser.objects.filter(is_active=True, role='Healthcare Provider', status='Active')
    patients = CustomUser.objects.filter(role='Patient')

    pending_users_count = pending_users.count()

    context = {
        'pending_users': pending_users,
        'active_users': active_users,
        'patients': patients,
        'pending_users_count': pending_users_count,
    }

    return render(request, 'CarePath/manage_users.html', context)

@login_required
def approve_account(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = True
    user.status = 'Active'
    user.save()
    messages.success(request, f"The account for {user.first_name} {user.last_name} has been approved.")
    return redirect('manage_users')




# Disable account (for Healthcare Provider)
@login_required
def disable_account(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    
    if user.is_staff:
        user.status = 'Disabled'
        user.is_active = False
        user.save()
        messages.success(request, f"{user.first_name} {user.last_name}'s account has been disabled.")
    else:
        messages.error(request, "You cannot disable a non-staff account.")
    
    return redirect('manage_users')



# Discharge patient
@login_required
def discharge_patient(request, patient_id):
    patient = get_object_or_404(CustomUser, id=patient_id, role='Patient')

    if not patient.is_staff:
        patient.status = 'Discharged'
        patient.is_active = True  # Patient can still log in
        patient.save()
        messages.success(request, f"{patient.first_name} {patient.last_name} has been discharged.")
    else:
        messages.error(request, "You cannot discharge a staff member.")
    
    return redirect('manage_users')


@login_required
def activate_patient(request, patient_id):
    patient = get_object_or_404(CustomUser, id=patient_id, role='Patient')

    if not patient.is_staff:
        patient.status = 'Active'
        patient.is_active = True  # Patient can log in again
        patient.save()
        messages.success(request, f"{patient.first_name} {patient.last_name} has been activated.")
    else:
        messages.error(request, "You cannot activate a staff member.")

    return redirect('manage_users')
