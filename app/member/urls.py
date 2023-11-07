from django.urls import path
from app.member import views, authentications

app_name = 'app.member'

urlpatterns = [
    path('login/', authentications.login, name='login'),
    path('register/', authentications.register, name='register'),
    path('verify/auth/', authentications.verify, name='verify'),
    path('resend_code/', authentications.resend_code, name='resend_code'),
    path('forgot-password/', authentications.forgot_password, name='forgot_password'),

    path('dashboard/activity/', views.member_dashboard_activity, name='member_dashboard_activity'),
    path('profile/', views.member_profile, name='member_profile'),
    path('profile/update/', views.member_profile_update, name='member_profile_update'),
    path('password/', views.member_profile_security, name='member_profile_security'),
]
