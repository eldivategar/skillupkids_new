from django.urls import path
from app.mitra import views, authentications

app_name = 'app.mitra'

urlpatterns = [
    path('login/', authentications.login, name='login'),    
    path('register/', authentications.register, name='register'),
    path('verify/auth/', authentications.verify_account, name='verify'),
    path('register/2/', authentications.register_2, name='register_2'),

    path('dashboard/activity/', views.mitra_dashboard_activity, name='mitra_dashboard_activity'),
    path('profile/', views.mitra_profile, name='mitra_profile'),
    path('profile/update/', views.mitra_profile_update, name='mitra_profile_update'),
    path('password/', views.mitra_profile_security, name='mitra_profile_security'),
]