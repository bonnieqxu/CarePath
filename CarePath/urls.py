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

    # info page
    path("info/", views.info, name="info"),
    path("mouthcare/", views.mouthcare, name="mouthcare"),
    path('mouthcare_pdf/', views.mouthcare_pdf, name='mouthcare_pdf'),
    path("drymouth/", views.drymouth, name="drymouth"),
    path('drymouth_pdf/', views.drymouth_pdf, name='drymouth_pdf'),
    path("sideeffect/", views.sideeffect, name="sideeffect"),
    path('sideeffect_pdf/', views.sideeffect_pdf, name='sideeffect_pdf'),



    path("mouthcare_post/", views.mouthcare_post, name="mouthcare_post"),
    path('mouthcare_post_pdf/', views.mouthcare_post_pdf, name='mouthcare_post_pdf'),




    # team page
    path("team/", views.team, name="team"),



    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    # path('logout/', views.logout, name='logout'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),


    # path('login/', auth_views.LoginView.as_view(template_name='CarePath/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

]

