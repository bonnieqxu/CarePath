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


def home(request):
    return render(request, 'CarePath/home.html')


def about(request):
    return render(request, "CarePath/about.html")

def contact(request):
    return render(request, "CarePath/contact.html")

def faq(request):
    return render(request, "CarePath/faq.html")

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'CarePath/register.html', {'form': form})

