from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.core.cache import cache

def _404(request, exception=None, requested_url=None):
    return render(request, 'errors/error-404.html')

def _500(request):
    return render(request, 'errors/error-500.html')

def coming_soon(request):
    return render(request, 'events/coming-soon.html')

def logout(request):
    logout(request)
    request.session.flush()
    cache.clear()
    return redirect('home')