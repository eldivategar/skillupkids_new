from app.models import ActivityList, Transaction
from django.utils import timezone

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