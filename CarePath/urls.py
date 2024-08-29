from django.urls import path
from django.contrib.auth import views as auth_views
from CarePath import views
# from CarePath.models import 




urlpatterns = [
    path('', views.home, name='home'),

    # journey page
    path("journey/", views.journey, name="journey"),   
    path("mdm/", views.mdm, name="mdm"),
    path("pre_dental/", views.pre_dental, name="pre_dental"),
    path("tx_sideeffect/", views.tx_sideeffect, name="tx_sideeffect"),
    path("mucositis/", views.mucositis, name="mucositis"),
    path("post_dental/", views.post_dental, name="post_dental"),
    path("discharge/", views.discharge, name="discharge"),

    path("info/", views.info, name="info"),
    path("team/", views.team, name="team"),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='CarePath/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

]

