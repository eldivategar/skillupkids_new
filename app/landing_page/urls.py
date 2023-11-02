from django.urls import path
from app.landing_page import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('verify/auth/', views.verify, name='verify'),
    path('logout/', views.logout, name='logout'),
]