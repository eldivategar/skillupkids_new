from app.models import Mitra, ActivityList

def get_my_activity(uuid, keyword=None, status=None):
    if keyword == None and status == None or status == 'all':
        get_all_activity = ActivityList.objects.filter(mitra_activity=uuid).order_by('-activity_id')

    elif keyword == None and status != None:
        get_all_activity = ActivityList.objects.filter(mitra_activity=uuid, activity_status=status).order_by('-activity_id')

    elif keyword != None and status == None:
        get_all_activity = ActivityList.objects.filter(mitra_activity=uuid, activity_name__icontains=keyword).order_by('-activity_id')

    elif keyword != None and status != None:
        get_all_activity = ActivityList.objects.filter(mitra_activity=uuid, activity_name__icontains=keyword, activity_status=status).order_by('-activity_id')
    
    all_data = []

    for activity in get_all_activity:
        mitra_data = Mitra.objects.get(name=activity.mitra_activity.name)
        activity_data = activity.activity_json()           
        
        all_data.append({
            'mitra': mitra_data,
            'activity': activity_data,
        })
    
    return all_data

def get_status():
    status = ['Pending', 'Ditolak', 'Terbit']
    return status