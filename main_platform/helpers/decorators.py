from django.shortcuts import redirect
from django.http import HttpResponse
from functools import wraps

def user_must_be_registered(view_func):
    def wrapper(request, *args, **kwargs):
        if 'unique_code' in request.session:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('Halaman tidak ditemukan!')
    return wrapper

def cek_user_session(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if 'customer_id' in request.session:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')
    return _wrapped_view