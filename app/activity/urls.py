from django.urls import path
from app.activity import views

# app_name = 'activity'

urlpatterns = [    
    path('class-list/', views.ClassList.as_view(), name='class_list'),
    path('class-list/<int:id>/<str:activity_name>', views.class_detail, name='class_detail'),
    path('chat-with-admin/<int:id>/<str:activity_name>', views.chat_to_admin, name='chat_to_admin'),
    path('buy-activity/<str:id>', views.buy_activity, name='buy_activity'),
]