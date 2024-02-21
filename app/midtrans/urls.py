from django.urls import path
from app.midtrans import tokenizer

urlpatterns = [
    path('midtrans-callback/', tokenizer.midtrans_callbackk, name='midtrans_callback'),
]