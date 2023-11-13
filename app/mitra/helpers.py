from app.models import Mitra, ActivityList, Transaction

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

def get_registered_member(activity_id):
    get_activity = Transaction.objects.filter(activity=activity_id)
    get_all_member = []

    for data in get_activity:
        member_data = data.member.member_json()
        get_all_member.append({
            'member': member_data,
            'transaction': data.transaction_json(),
            'activity': data.activity.activity_json(),
        })
    
    return get_all_member