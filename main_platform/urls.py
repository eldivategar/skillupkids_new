from django.urls import path
from main_platform import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('verify/', views.verify, name='verify'),
    path('verify/auth/<str:unique_code>/', views.verify, name='verify'),
    path('logout/', views.logout, name='logout'),
]