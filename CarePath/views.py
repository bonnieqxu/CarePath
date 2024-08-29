import re
from django.utils.timezone import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect

# from CarePath.forms import LogMessageForm
# from CarePath.models import LogMessage
# from django.views.generic import ListView

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Replace the existing home function with the one below
# class HomeListView(ListView):
#     """Renders the home page, with a list of all messages."""
#     model = LogMessage

#     def get_context_data(self, **kwargs):
#         context = super(HomeListView, self).get_context_data(**kwargs)
#         return context


#----------------------- visitor related views  -------------------------------

# landing page
def home(request):
    return render(request, 'CarePath/home.html')

# healthcare journey related views
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


def team(request):
    return render(request, "CarePath/team.html")

def info(request):
    return render(request, "CarePath/info.html")

# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             return redirect('login')
#     else:
#         form = UserCreationForm()
    
#     return render(request, 'CarePath/register.html', {'form': form})

def register(request):
    return render(request, "CarePath/register.html")

