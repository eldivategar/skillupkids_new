from django.shortcuts import render, redirect

def _404(request, exception=None, requested_url=None):
    return render(request, 'errors/error-404.html')

def _500(request):
    return render(request, 'errors/error-500.html')

def coming_soon(request):
    return render(request, 'events/coming-soon.html')

def logout(request):
    request.session.flush()
    return redirect('home')