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
    path('dashboard/activity/detail/<str:id>/<str:activity>', views.view_activity, name='view_activity'),
    path('profile/', views.member_profile, name='member_profile'),
    path('profile/update/', views.member_profile_update, name='member_profile_update'),
    path('security/', views.member_profile_security, name='member_profile_security'),
    path('security/update/', views.member_profile_security_update, name='member_profile_security_update'),
    path('transactions/', views.transactions, name='transactions'),
    path('chat-to-pay/<str:transaction_id>', views.chat_to_pay, name='chat_to_pay'),
    path('chat-to-admin/', views.chat_to_admin, name='chat_to_admin'),
    path('rating/<str:activity_id>', views.rating, name='rating'),
]
