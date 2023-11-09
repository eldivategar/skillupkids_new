from django.shortcuts import render, redirect
from app.helpers.utils import get_member_data, get_mitra_data
from app.activity.helpers import get_category, get_new_activity, get_testimonial

def home(request):
    category = get_category()
    new_activity = get_new_activity()
    testimonials = get_testimonial()

    if 'customer_id' not in request.session:
        return render(request, 'landing_page/index.html', {'category': category, 'new_activity': new_activity, 'testimonials': testimonials})
    else:
        customer = request.session.get('customer_id')
        if customer[:2] == 'mi' :
            data = get_mitra_data(request)
            return render(request, 'landing_page/index.html', {'data': data, 'category': category, 'new_activity': new_activity, 'testimonials': testimonials})
        elif customer[:2] == 'me':
            data = get_member_data(request)
            return render(request, 'landing_page/index.html', {'data': data, 'category': category, 'new_activity': new_activity, 'testimonials': testimonials})

def about(request):
    if 'customer_id' not in request.session:
        return render(request, 'landing_page/about.html')
    else:
        customer = request.session.get('customer_id')
        if customer[:2] == 'mi' :
            data = get_mitra_data(request)
            return render(request, 'landing_page/about.html', {'data': data})
        elif customer[:2] == 'me':
            data = get_member_data(request)
            return render(request, 'landing_page/about.html', {'data': data})

def contact(request):
    if 'customer_id' not in request.session:
        return render(request, 'landing_page/contact.html')
    else:
        customer = request.session.get('customer_id')
        if customer[:2] == 'mi' :
            data = get_mitra_data(request)
            return render(request, 'landing_page/contact.html', {'data': data})
        elif customer[:2] == 'me':
            data = get_member_data(request)
            return render(request, 'landing_page/contact.html', {'data': data})