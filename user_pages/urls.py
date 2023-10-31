from django.urls import path
from user_pages import views
from django.contrib.auth.decorators import login_required

app_name = 'user_pages'

urlpatterns = [
    path('activity/', views.member_activity, name='member_activity'),
    path('profile/', views.member_profile, name='member_profile'),
    path('profile/update/', views.member_profile_update, name='member_profile_update'),
]
