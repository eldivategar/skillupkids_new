from django.urls import path
from app.activity import views

# app_name = 'activity'

urlpatterns = [    
    path('class-list/', views.class_list, name='class_list'),
    path('class-list/<int:id>/<str:activity_name>', views.class_detail, name='class_detail'),    
]