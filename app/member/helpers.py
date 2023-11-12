from app.models import ActivityList, Transaction
from django.utils import timezone
from datetime import timedelta

def get_transactions(id):
    transactions = Transaction.objects.filter(member=id).order_by('-date')
    transactions_data = []    
    check_payment_status(id)
    for transaction in transactions:
        activity = ActivityList.objects.filter(activity_id=transaction.activity.activity_id)
        
        transaction_data = transaction.transaction_json()
        transactions_data.append({
            'transaction': transaction_data,
            'activity': activity[0].activity_json()
        })

    return transactions_data  

def check_payment_status(id):
    transactions = Transaction.objects.filter(member=id).order_by('-date')
    current_time = timezone.now()

    for transaction in transactions:
        payment_due_time = transaction.date + timedelta(minutes=1)
        remaining_time = payment_due_time - current_time
        if remaining_time.total_seconds() <= 0:
            transaction.status = 'Gagal'