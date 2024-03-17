from django.shortcuts import redirect
from django.http import HttpResponse
from django.urls import reverse
from functools import wraps

def user_must_be_registered(view_func):
    def wrapper(request, *args, **kwargs):
        if 'unique_code' in request.session:
            return view_func(request, *args, **kwargs)
        else:
            requested_url = request.path
            return redirect(reverse('notfound', kwargs={'requested_url': requested_url}))
    return wrapper

def cek_member_session(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if 'customer_id' in request.session and request.session['customer_id'][:2] == 'me':
            return view_func(request, *args, **kwargs)
        else:
            request.session['next_url'] = request.path
            return redirect('app.member:login')
    return _wrapped_view

def cek_mitra_session(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if 'customer_id' in request.session and request.session['customer_id'][:2] == 'mi':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('app.mitra:login')
    return _wrapped_view