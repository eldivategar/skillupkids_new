from app.models import ActivityList, Transaction, Mitra

def get_member_activity(id):
    get_activites = Transaction.objects.filter(member=id, status='Sukses').order_by('-date')
    activites_data = []

    for activity in get_activites:
        data = activity.activity.activity_json()
        mitra_data = Mitra.objects.get(name=data['mitra_activity'])
        activites_data.append({
            'activity': data,
            'mitra': mitra_data.mitra_json(),
        })
    # print(activites_data)
    return activites_data
def get_transactions(id):
    transactions = Transaction.objects.filter(member=id).order_by('-date')
    transactions_data = []    
    
    for transaction in transactions:
        activity = ActivityList.objects.filter(activity_id=transaction.activity.activity_id)
        
        transaction_data = transaction.transaction_json()
        transactions_data.append({
            'transaction': transaction_data,
            'activity': activity[0].activity_json()
        })

    return transactions_data