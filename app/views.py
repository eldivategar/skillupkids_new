from django.shortcuts import render

def _404(request, exception):
    return render(request, 'errors/error-404.html')

def _500(request):
    return render(request, 'errors/error-500.html')