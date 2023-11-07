from django.urls import path
from app.mitra import views, authentications

app_name = 'app.mitra'

urlpatterns = [
    path('login/', authentications.login, name='login'),    
    path('register/', authentications.register, name='register'),
    path('verify/auth/', authentications.verify_account, name='verify'),
    path('register/2/', authentications.register_2, name='register_2'),
    path('resend_code/', authentications.resend_code, name='resend_code'),

    path('dashboard/list-of-activity/', views.mitra_dashboard_activity_list, name='mitra_dashboard_activity_list'),
    path('dashboard/create-new-activity/', views.mitra_create_new_activity, name='mitra_create_new_activity'),


    path('profile/', views.mitra_profile, name='mitra_profile'),
    path('profile/update/', views.mitra_profile_update, name='mitra_profile_update'),
    path('sosmed/', views.mitra_sosmed, name='mitra_sosmed'),
    path('sosmed/update', views.mitra_sosmed_update, name='mitra_sosmed_update'),
    path('password/', views.mitra_profile_security, name='mitra_profile_security'),
]