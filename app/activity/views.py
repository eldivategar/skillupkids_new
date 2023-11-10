from django.shortcuts import render, redirect
from django.http import HttpResponse
from app.helpers.utils import get_member_data, get_mitra_data
from .helpers import get_activity_detail, get_activity_list, get_category
from app.helpers.utils import redirect_to_whatsapp
from app.models import Member
from app.activity.helpers import get_activity_detail
from django.utils.html import escape

def class_list(request):
    if request.method == 'GET':
        category = request.GET.get('category')
        keyword = request.GET.get('keyword')        
        
        if category == None and keyword == None:
            list_of_activity = get_activity_list(category='all')

        elif category == None and keyword != None:
            list_of_activity = get_activity_list(keyword=keyword)
        
        elif category != None and keyword == None:
            list_of_activity = get_activity_list(category=category)
        
        elif category != None and keyword != None:
            list_of_activity = get_activity_list(category=category, keyword=keyword)                

        categories = get_category()

        if 'customer_id' not in request.session:
            return render(request, 'activity/class-list.html', {'list_of_activity': list_of_activity, 'category': categories})
        else:
            customer = request.session.get('customer_id')
            if customer[:2] == 'mi' :
                data = get_mitra_data(request)
                return render(request, 'activity/class-list.html', {'data': data, 'list_of_activity': list_of_activity, 'category': categories})
            elif customer[:2] == 'me':
                data = get_member_data(request)
                return render(request, 'activity/class-list.html', {'data': data, 'list_of_activity': list_of_activity, 'category': categories})
        
def class_detail(request, id, activity_name):
    if request.method == 'GET':        
        data_detail_activity = get_activity_detail(id)
        
        if 'customer_id' not in request.session:
            return render(request, 'activity/activity-details.html', {'data_detail_activity': data_detail_activity})
        else:
            customer = request.session.get('customer_id')
            if customer[:2] == 'mi' :
                data = get_mitra_data(request)
                return render(request, 'activity/activity-details.html', {'data': data, 'data_detail_activity': data_detail_activity})
            elif customer[:2] == 'me':
                data = get_member_data(request)
                return render(request, 'activity/activity-details.html', {'data': data, 'data_detail_activity': data_detail_activity})

def buy_activity(request, id, activity_name):
    if request.method == 'GET':
        customer_id = request.session.get('customer_id')[2:]
        member = Member.objects.get(uuid=customer_id)
        activity = get_activity_detail(id)
        activity_name = activity['activity']['activity_name']
        activity_category = activity['activity']['category']

        message = f'Halo admin %F0%9F%98%8A \nSaya atas nama {member} mau daftar kegiatan {activity_name} dengan kategori {activity_category}!'
        return redirect_to_whatsapp(message)
        