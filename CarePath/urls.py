from django.urls import path
from django.contrib.auth import views as auth_views
# from . import views
from CarePath import views
# from CarePath.models import LogMessage


# home_list_view = views.HomeListView.as_view(
#     queryset=LogMessage.objects.order_by("-log_date")[:5],  # :5 limits the results to the five most recent
#     context_object_name="message_list",
#     template_name="CarePath/home.html",
# )

urlpatterns = [
    # path("", home_list_view, name="home"),
    path('', views.home, name='home'),
    # path("hello/<name>", views.hello_there, name="hello_there"),
    path("about/", views.about, name="about"),
    path("faq/", views.faq, name="faq"),
    path("contact/", views.contact, name="contact"),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='CarePath/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    # path("log/", views.log_message, name="log"),
]

