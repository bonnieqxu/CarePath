from django.conf.urls.i18n import set_language
from django.urls import path
from django.contrib.auth import views as auth_views
from CarePath import views
from .views import PatientPasswordChangeView, ProviderPasswordChangeView, AdminPasswordChangeView, activate_user






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

    path('activate/<uidb64>/<token>/', activate_user, name='activate'),
    path('activate/<uidb64>/<token>/', views.activate_user, name='activate_user'),
    path('confirm-activation/<int:user_id>/', views.confirm_account_activation, name='confirm_account_activation'),
    # path('account_pending/', views.account_pending, name='account_pending'),

    # dashboards
    path('dashboard/', views.dashboard, name='dashboard'),
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('provider/dashboard/', views.provider_dashboard, name='provider_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # patient dashboard functions
    path('patient_profile/<int:id>/', views.patient_profile, name='patient_profile'),
    path('patient_password/', PatientPasswordChangeView.as_view(), name='patient_password'),
    path('patient_appt/', views.patient_appt, name='patient_appt'),
    path('view_provider_details/<int:provider_id>/', views.view_provider_details, name='view_provider_details'),

    path('patient/communication/', views.patient_communication, name='patient_communication'),
    path('patient_messages/', views.patient_messages, name='patient_messages'),
    path('mark_as_read/<int:message_id>/', views.mark_as_read, name='mark_as_read'),
    path('mark_as_unread/<int:message_id>/', views.mark_as_unread, name='mark_as_unread'),
    path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),

    path('patient_reminders/', views.patient_reminders, name='patient_reminders'),
    path('reminder/read/<int:reminder_id>/', views.mark_reminder_as_read, name='mark_reminder_as_read'),
    path('reminder/unread/<int:reminder_id>/', views.mark_reminder_as_unread, name='mark_reminder_as_unread'),
    path('reminder/delete/<int:reminder_id>/', views.delete_reminder, name='delete_reminder'),

    path('patient_feedback/', views.patient_feedback, name='patient_feedback'),
    path('submit_feedback/', views.submit_feedback, name='submit_feedback'),

    # healthcare provider dashboard functions
    path('provider_profile/', views.provider_profile, name='provider_profile'),
    path('provider_password/', ProviderPasswordChangeView.as_view(), name='provider_password'),
    path('provider_appt/', views.provider_appt, name='provider_appt'),
    path('view_more_appt_info/<int:patient_id>/<int:appointment_id>/', views.view_more_appt_info, name='view_more_appt_info'),
    path('edit_appt/<int:patient_id>/<int:appointment_id>/', views.edit_appt, name='edit_appt'),

    path('provider_search_pt/', views.provider_search_pt, name='provider_search_pt'),
    path('provider_view_pt/<int:patient_id>/', views.provider_view_pt, name='provider_view_pt'),
    path('book_pt_appointment/<int:patient_id>/', views.book_pt_appointment, name='book_pt_appointment'),
    path('cancel_appt/<int:appointment_id>/', views.cancel_appt, name='cancel_appt'),

    path('provider/feedback/', views.provider_feedback, name='provider_feedback'),
    path('feedback/read/<int:feedback_id>/', views.mark_feedback_as_read, name='mark_feedback_as_read'),
    path('feedback/unread/<int:feedback_id>/', views.mark_feedback_as_unread, name='mark_feedback_as_unread'),
    path('feedback/delete/<int:feedback_id>/', views.delete_feedback, name='delete_feedback'),

    # admin dashboard functions
    path('admin_profile/', views.admin_profile, name='admin_profile'),
    path('admin_password/', AdminPasswordChangeView.as_view(), name='admin_password'),
    path('admin/appointments/', views.all_appointments, name='all_appointments'),
    path('admin/search_pt/', views.admin_search_pt, name='admin_search_pt'),
    path('admin/view_pt/<int:id>/', views.admin_view_pt, name='admin_view_pt'),
    path('admin/book_pt_appointment/<int:patient_id>/', views.admin_book_pt_appointment, name='admin_book_pt_appointment'),
    path('admin/cancel_appt/<int:appointment_id>/', views.admin_cancel_appt, name='admin_cancel_appt'),
    path('admin/edit_appt/<int:patient_id>/<int:appointment_id>/', views.admin_edit_appt, name='admin_edit_appt'),
   
    path('manage_users/', views.manage_users, name='manage_users'),
    path('approve_account/<int:user_id>/', views.approve_account, name='approve_account'),
    path('disable_account/<int:user_id>/', views.disable_account, name='disable_account'),
    path('discharge_patient/<int:patient_id>/', views.discharge_patient, name='discharge_patient'),
    path('activate_patient/<int:patient_id>/', views.activate_patient, name='activate_patient'),



    path('i18n/setlang/', set_language, name='set_language'),

]

