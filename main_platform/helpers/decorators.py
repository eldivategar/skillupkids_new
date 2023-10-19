from django.shortcuts import redirect
from django.http import HttpResponse

def user_must_be_registered(view_func):
    def wrapper(request, *args, **kwargs):
        if 'unique_code' in request.session:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('Halaman tidak ditemukan!')
    return wrapper
