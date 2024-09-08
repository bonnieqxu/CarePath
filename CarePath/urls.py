from django.urls import path
from django.contrib.auth import views as auth_views
from CarePath import views
from .views import CustomPasswordChangeView
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
    path("speech/", views.speech, name="speech"),
    path('speech_pdf/', views.speech_pdf, name='speech_pdf'),
    path('stretch_pdf/', views.stretch_pdf, name='stretch_pdf'),
    path("diet/", views.diet, name="diet"),
    path('diet_pdf/', views.diet_pdf, name='diet_pdf'),
    path("mouthcare_post/", views.mouthcare_post, name="mouthcare_post"),
    path('mouthcare_post_pdf/', views.mouthcare_post_pdf, name='mouthcare_post_pdf'),




    # team page
    path("team/", views.team, name="team"),


    # auth
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # dashboards
    path('dashboard/', views.dashboard, name='dashboard'),
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('provider/dashboard/', views.provider_dashboard, name='provider_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # patient dashboard functions
    # path('patient_profile/', views.patient_profile, name='patient_profile'),
    path('patient_profile/<int:id>/', views.patient_profile, name='patient_profile'),
    path('patient_password/', CustomPasswordChangeView.as_view(), name='patient_password'),
    path('patient_appt/', views.patient_appt, name='patient_appt'),

    # healthcare provider dashboard functions
    path('provider_profile/', views.provider_profile, name='provider_profile'),
    path('provider_password/', CustomPasswordChangeView.as_view(), name='provider_password'),
    path('provider_appt/', views.provider_appt, name='provider_appt'),
    path('provider_search_pt/', views.provider_search_pt, name='provider_search_pt'),
    # path('provider_view_pt/<int:id>/', views.provider_view_pt, name='patient_profile'),
    path('provider_view_pt/<int:patient_id>/', views.provider_view_pt, name='provider_view_pt'),

    path('book_pt_appointment/<int:patient_id>/', views.book_pt_appointment, name='book_pt_appointment'),

]

