import re
import os

from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.views import PasswordChangeView

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import CustomUser


from django.utils.timezone import datetime



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
def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        address = request.POST['address']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        role = request.POST['role']

        if password != confirm_password:
            return render(request, 'CarePath/register.html', {'error': "Passwords do not match"})

        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'CarePath/register.html', {'error': "Email already in use"})

        # Create the new user
        user = CustomUser.objects.create_user(
            username=email,  # email is used as the username
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            address=address,
            password=password,
            role=role,
        )

        user.save()
        group = Group.objects.get(name=role)
        user.groups.add(group)

        return redirect('login')  # Redirect to the login page after successful registration

    return render(request, 'CarePath/register.html')




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
@login_required
def patient_profile(request):
    user = request.user

    if request.method == "POST":
        # update info
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.phone_number = request.POST['phone_number']
        user.address = request.POST['address']
        user.save()

        messages.success(request, "Your profile has been updated successfully!")
        return redirect('patient_profile')  

    return render(request, 'CarePath/patient_profile.html', {
        'user': user,
    })


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'CarePath/patient_password.html'
    success_url = reverse_lazy('patient_profile')

    def form_valid(self, form):
        messages.success(self.request, 'Your password has been updated successfully!')
        return super().form_valid(form)