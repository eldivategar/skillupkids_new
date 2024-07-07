from django.urls import path
from app.landing_page import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about-us/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),    
    path('blog/', views.blog, name='blog'),
    path('blog/<int:blog_id>/<str:blog_title>', views.blog_detail, name='blog_detail'),
    path('terms', views.terms_of_use, name='terms')
]