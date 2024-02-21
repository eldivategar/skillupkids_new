from app.models import ActivityList, Transaction, Mitra, Testimonial
from django.shortcuts import get_object_or_404
from django.core import serializers

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

def get_transaction(cust_id, transaction_id):
    get_transaction = Transaction.objects.filter(member=cust_id, transaction_id=transaction_id)
    transaction_data = []
    
    for transaction in get_transaction:
        data = transaction.transaction_json()
        transaction_data.append(data)

    return transaction_data


def get_all_transactions(id):
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

def check_testimoni_member(member_id, activity_id):
    testimoni = Testimonial.objects.filter(member=member_id, activity=activity_id)
    if testimoni:
        return True
    else:
        return False    