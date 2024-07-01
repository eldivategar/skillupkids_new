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


def get_all_transactions(member_id):
    transactions = Transaction.objects.filter(member=member_id).select_related('activity').order_by('-date')
    activities = ActivityList.objects.filter(activity_id__in=transactions.values_list('activity_id', flat=True))
    activity_dict = {activity.activity_id: activity.activity_json() for activity in activities}
    
    transactions_data = []
    for transaction in transactions:
        transaction_data = transaction.transaction_json()
        activity_data = activity_dict.get(transaction.activity.activity_id, {})
        transactions_data.append({
            'transaction': transaction_data,
            'activity': activity_data
        })

    return transactions_data


def check_testimoni_member(member_id, activity_id):
    testimoni = Testimonial.objects.filter(member=member_id, activity=activity_id)
    if testimoni:
        return True
    else:
        return False    