from django.shortcuts import render, redirect
from app.helpers.utils import get_member_data, get_mitra_data

def home(request):
    if 'customer_id' not in request.session:
        return render(request, 'landing_page/index.html')
    else:
        customer = request.session.get('customer_id')
        if customer[:2] == 'mi' :
            data = get_mitra_data(request)
            return render(request, 'landing_page/index.html', {'data': data})
        elif customer[:2] == 'me':
            data = get_member_data(request)
            return render(request, 'landing_page/index.html', {'data': data})

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

def class_list(request):
    if 'customer_id' not in request.session:
        return render(request, 'landing_page/class-list.html')
    else:
        customer = request.session.get('customer_id')
        if customer[:2] == 'mi' :
            data = get_mitra_data(request)
            return render(request, 'landing_page/class-list.html', {'data': data})
        elif customer[:2] == 'me':
            data = get_member_data(request)
            return render(request, 'landing_page/class-list.html', {'data': data})