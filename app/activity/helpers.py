from app.models import Member, Mitra, ActivityList
from django.shortcuts import get_object_or_404

def get_activity_detail(id):
    detail_activity = get_object_or_404(ActivityList, activity_id=id).activity_json()
    mitra_data = Mitra.objects.get(name=detail_activity['mitra_activity']).mitra_json()
        
    data_detail_activity = {
        'mitra': mitra_data,
        'activity': detail_activity
    }
    return data_detail_activity

def get_activity_list(category, keyword=None):
    if category == 'all' and keyword == None:
        get_all_activity = ActivityList.objects.filter(activity_status='terbit')
        all_data = []

        for activity in get_all_activity:
            mitra_data = Mitra.objects.get(name=activity.mitra_activity.name)
            activity_data = activity.activity_json()           
            
            all_data.append({
                'mitra': mitra_data,
                'activity': activity_data,
            })        
        
        return all_data

    elif category == 'all' and keyword != None:
        get_all_activity = ActivityList.objects.filter(activity_status='terbit', activity_name__icontains=keyword)
        all_data = []

        for activity in get_all_activity:
            mitra_data = Mitra.objects.get(name=activity.mitra_activity.name)
            activity_data = activity.activity_json()           
            
            all_data.append({
                'mitra': mitra_data,
                'activity': activity_data,
            })        
        
        return all_data

    elif category != 'all' and keyword == None:
        get_all_activity = ActivityList.objects.filter(activity_status='terbit', category=category)
        all_data = []

        for activity in get_all_activity:
            mitra_data = Mitra.objects.get(name=activity.mitra_activity.name)
            activity_data = activity.activity_json()           
            
            all_data.append({
                'mitra': mitra_data,
                'activity': activity_data,
            })        
        
        return all_data

    elif category != 'all' and keyword != None:
        get_all_activity = ActivityList.objects.filter(activity_status='terbit', category=category, activity_name__icontains=keyword)
        all_data = []

        for activity in get_all_activity:
            mitra_data = Mitra.objects.get(name=activity.mitra_activity.name)
            activity_data = activity.activity_json()           
            
            all_data.append({
                'mitra': mitra_data,
                'activity': activity_data,
            })        
        
        return all_data
     
    
def get_category():
    get_all_category = ActivityList.objects.filter(activity_status='terbit').values_list('category', flat=True).distinct()
    categories_data = set()
    
    for category in get_all_category:
        categories_data.add(category)
        
    categories_list = sorted(list(categories_data))
    
    return categories_list

def get_new_activity():
    get_all_activity = ActivityList.objects.filter(activity_status='terbit').order_by('-activity_id')
    all_data = []

    for activity in get_all_activity:
        mitra_data = Mitra.objects.get(name=activity.mitra_activity.name)
        activity_data = activity.activity_json()           
        
        all_data.append({
            'mitra': mitra_data,
            'activity': activity_data,
        })        

    return all_data

def get_searched_activity(keyword):
    get_all_activity = ActivityList.objects.filter(activity_status='terbit', activity_name__icontains=keyword)
    all_data = []

    for activity in get_all_activity:
        mitra_data = Mitra.objects.get(name=activity.mitra_activity.name)
        activity_data = activity.activity_json()           
        
        all_data.append({
            'mitra': mitra_data,
            'activity': activity_data,
        })        

    return all_data