from django.urls import path
from app.member import views

app_name = 'app.member'

urlpatterns = [
    path('dashboard/activity/', views.member_dashboard_activity, name='member_dashboard_activity'),
    path('profile/', views.member_profile, name='member_profile'),
    path('profile/update/', views.member_profile_update, name='member_profile_update'),
    path('password/', views.member_profile_security, name='member_profile_security'),
]
