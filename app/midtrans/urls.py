from django.urls import path
from app.midtrans import tokenizer

urlpatterns = [
    path('midtrans-callback/', tokenizer.midtrans_callback, name='midtrans_callback'),
]