import logging

logger = logging.getLogger(__name__)

import os
import midtransclient
from django.shortcuts import redirect
from app.models import Transaction
from django.http import HttpResponse
from skillupkids import settings
from django.shortcuts import get_object_or_404
from app.models import Member, Mitra
from app.activity.helpers import get_activity_detail
from app.helpers.utils import send_email


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
    is_production=True,
    server_key=settings.MIDTRANS_SERVER_KEY,
    client_key=settings.MIDTRANS_CLIENT_KEY
)


def generate_token_midtrans(order_id, gross_amount, name, email, phone, item_id, item_name, quantity=1):
    # Create Snap API instance
    # Build API parameter
    try:
        # Mengubah gross_amount menjadi integer
        # gross_amount = int(float(gross_amount) * 1000)
        gross_amount = str(gross_amount)
    except ValueError:
        logger.error(f"Nilai gross_amount tidak valid: {gross_amount}")
        raise ValueError("Nilai gross_amount tidak valid")
    
    param = {
        "transaction_details": {
            "order_id": order_id,
            "gross_amount": gross_amount
        }, 
        "page_expiry": {
            "duration": 1,
            "unit": "hours"
        },
          "expiry": {
            "duration": 1,
            "unit": "hours"
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
        },
    }
    transaction = snap.create_transaction(param)
    transaction_token = transaction['token']

    return transaction_token

def midtrans_callback(request):
    if request.method == 'POST':
        notification = request.body.decode('utf-8')

        response = snap.transactions.notification(notification)
                
        order_id = response['order_id']
        transaction_status = response['transaction_status']
        
        if transaction_status == 'settlement' or transaction_status == 'capture':
            transaction = Transaction.objects.get(transaction_id=order_id)
            transaction.status = 'Sukses'
            transaction.save()
            
            try:
                activity = get_activity_detail(transaction.activity.activity_id)
                activity_details = activity['activity']
                activity_name = activity_details['activity_name']
                member = get_object_or_404(Member, uuid=transaction.member.uuid)
                mitra = get_object_or_404(Mitra, uuid=transaction.mitra.uuid)
                
                context = {
                    'data': {
                        'tanggal': transaction.date.strftime('%d %B %Y %H:%M:%S'),
                        'nama_kegiatan': activity_name,
                        'waktu_kegiatan': activity_details['activity_informations']['day'],
                        'member': {
                            'nama': member.name,
                            'email': member.email,
                            'no_hp': member.number,
                            'alamat': member.address,
                        },
                        'mitra': {
                            'nama': mitra.name,
                            'email': mitra.email,
                            'no_hp': mitra.number,
                            'alamat': mitra.address,                                
                        }
                    }
                }
                subject_mitra = 'Notifikasi Pembelian Aktivitas'
                receiver_mitra = mitra.email
                send_email(subject_mitra, receiver_mitra, context, 'new_activity')
                return HttpResponse(status=200)
            except Exception as e:
                logger.error(f"Error saat mengirim email notifikasi: {e}")
                return HttpResponse(status=200)
        
        # handle transaction status if failed
        elif transaction_status == 'deny' or transaction_status == 'cancel' or transaction_status == 'expire':
            transaction = Transaction.objects.get(transaction_id=order_id)
            transaction.status = 'Gagal'
            transaction.save()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=200)