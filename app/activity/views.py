from django.shortcuts import render, redirect, get_object_or_404
from app.helpers.utils import get_member_data, get_mitra_data
from app.models import Member, Mitra, ActivityList
from .helpers import get_activity_list

def class_list(request):
    if request.method == 'GET':
        list_of_activity, categories = get_activity_list()
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
        detail_activity = get_object_or_404(ActivityList, activity_id=id).activity_json()
        mitra_data = Mitra.objects.get(name=detail_activity['mitra_activity']).mitra_json()
        
        data_detail_activity = {
            'mitra': mitra_data,
            'activity': detail_activity
        }

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
