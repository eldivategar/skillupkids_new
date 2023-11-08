from app.models import Member, Mitra, ActivityList

def get_activity_list():
    get_all_activity = ActivityList.objects.filter(activity_status='terbit')
    all_data = []
    categories_data = set()

    for activity in get_all_activity:
        mitra_data = Mitra.objects.get(name=activity.mitra_activity.name)
        activity_data = activity.activity_json()
        category = activity.category
        categories_data.add(category)
        
        all_data.append({
            'mitra': mitra_data,
            'activity': activity_data,
        })        
    categories_list = list(categories_data)
    return all_data, categories_list