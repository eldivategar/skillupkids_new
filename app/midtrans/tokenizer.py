import os
import midtransclient
from decimal import Decimal
from django.http import HttpResponse
from app.models import Transaction
from skillupkids import settings


def get_current_environment():
    django_settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', None)
    if django_settings_module:
        if 'dev' in django_settings_module:
            return 'Development'
        elif 'prod' in django_settings_module:
            return 'Production'
        else:
            return 'Unknown'
    else:
        return 'Environment not set'

current_environment = get_current_environment()
if current_environment == 'Development':
    is_production = False
else:
    is_production = True

snap = midtransclient.Snap(
    # Set to true if you want Production Environment (accept real transaction).
    is_production=is_production,
    server_key=settings.MIDTRANS_SERVER_KEY,
)

def generate_token_midtrans(order_id, gross_amount, name, email, phone, item_id, item_name, quantity=1):
    # Create Snap API instance
    # Build API parameter
    gross_amount = int(gross_amount * 1000)
    param = {
        "transaction_details": {
            "order_id": order_id,
            "gross_amount": gross_amount
        }, 
        "item_details": [
            {
                "id": item_id,
                "price": gross_amount,
                "quantity": quantity,
                "name": item_name
            }
        ],
        "customer_details":{
            "first_name": name,
            "email": email,
            "phone": phone
        }
    }

    transaction = snap.create_transaction(param)
    transaction_token = transaction['token']

    print(transaction_token)
    return transaction_token

def midtrans_callbackk(request):
    if request.method == 'POST':
        notification = request.body.decode('utf-8')

        response = snap.transactions.notification(notification)
                
        order_id = response['order_id']
        transaction_status = response['transaction_status']
        
        if transaction_status == 'settlement' or transaction_status == 'capture':
            transaction = Transaction.objects.get(transaction_id=order_id)
            transaction.status = 'Sukses'
            transaction.save()
            return HttpResponse(status=200)