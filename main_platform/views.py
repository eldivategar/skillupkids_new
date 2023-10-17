from django.shortcuts import render, redirect

def home(request):
    return render(request, 'landing_page/index.html')

def about(request):
    return render(request, 'landing_page/about.html')

def contact(request):
    return render(request, 'landing_page/contact.html')

def page_not_found(request, exception):
    return render(request, 'errors/404.html')