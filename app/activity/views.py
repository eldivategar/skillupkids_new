from django.shortcuts import render, redirect
from django.http import HttpResponse
from app.helpers.utils import get_member_data, get_mitra_data
from .helpers import get_activity_detail, get_activity_list, get_category
from app.helpers.utils import redirect_to_whatsapp
from app.models import Member, Transaction, Mitra
from app.activity.helpers import get_activity_detail
from app.helpers.decorators import cek_member_session
from django.utils import timezone
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from app.transaction.transaction import generate_transaction_id
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.shortcuts import get_object_or_404
from app.views import _500

class ClassList(View):
    @method_decorator(cache_page(60*60*24))
    def get(self, request):
        category = request.GET.get('category', 'all')
        keyword = request.GET.get('keyword', None)

        if category == 'all' and keyword == None:
            list_of_activity = cache.get('list_of_activity')
            if list_of_activity == None:
                list_of_activity = get_activity_list(category='all')
                cache.set('list_of_activity', list_of_activity, 60*60*24)
        
        else:
            list_of_activity = get_activity_list(category, keyword)               

        categories = get_category()

        customer_id = request.session.get('customer_id')

        if not customer_id:
            return render(request, 'activity/class-list.html', {'list_of_activity': list_of_activity, 'category': categories})
        else:
            if customer_id.startswith('mi'):
                data = get_mitra_data(request)
            elif customer_id.startswith('me'):
                data = get_member_data(request)            
            return render(request, 'activity/class-list.html', {'data': data, 'list_of_activity': list_of_activity, 'category': categories})


@cache_page(60*60*24)              
def class_detail(request, id, activity_name):
    if request.method == 'GET':        
        data_detail_activity = get_activity_detail(id)
        customer_id = request.session.get('customer_id')
        
        if not customer_id:
            return render(request, 'activity/activity-details.html', {'data_detail_activity': data_detail_activity})

        data = get_mitra_data(request) if customer_id.startswith('mi') else get_member_data(request)
        
        return render(request, 'activity/activity-details.html', {'data': data, 'data_detail_activity': data_detail_activity})

def chat_to_admin(request, id, activity_name):
    if request.method == 'GET':
        activity = get_activity_detail(id)
        activity_name = activity['activity']['activity_name']
        activity_category = activity['activity']['category']

        try:            
            customer_id = request.session.get('customer_id')[2:]
            member = get_object_or_404(Member, uuid=customer_id)

            message = f'Halo admin %F0%9F%98%8A \nSaya atas nama {member.name} mau daftar kegiatan {activity_name} dengan kategori {activity_category}!'
        except:
            message = f'Halo admin %F0%9F%98%8A \nSaya mau daftar kegiatan {activity_name} dengan kategori {activity_category}!'

        return redirect_to_whatsapp(message)

    
from app.midtrans.tokenizer import generate_token_midtrans
from app.transaction.transaction import generate_transaction_id
@cek_member_session
def buy_activity(request, id):
    if request.method == 'GET':
        customer_id = request.session.get('customer_id')[2:]
        member = Member.objects.get(uuid=customer_id)    
        activity = get_activity_detail(int(id))

        activity_id = activity['activity']['activity_id']
        activity_name = activity['activity']['activity_name']
        mitra = Mitra.objects.get(uuid=activity['mitra']['uuid'])
        price = activity['activity']['activity_informations']['price']

        transaction_id = generate_transaction_id()

        if price == 0:
            is_free = True
            status = 'Sukses'
            metode = '-'
        else:
            is_free = False
            status = 'Menunggu Pembayaran'
            metode = 'Transfer Bank'
            token = generate_token_midtrans(transaction_id, price, member.name, member.email, member.number, activity_id, activity_name)
            
        transaction = Transaction.objects.create(
            transaction_id=transaction_id,
            member=member,
            mitra=mitra,
            activity_id=activity_id,
            is_free=is_free,
            total_price=price,
            status=status,
            payment_method=metode,
            token=token
            # expired_at=expired_at 
        )
        transaction.save()
        print(token)
        return redirect('app.member:transactions')        


# @cek_member_session
# def buy_activity(request, id):
#     if request.method == 'GET':
#         customer_id = request.session.get('customer_id')[2:]
#         member = get_object_or_404(Member, uuid=customer_id)
#         activity = get_activity_detail(int(id))

#         activity_id = activity['activity']['activity_id']
#         mitra = get_object_or_404(Mitra, uuid=activity['mitra']['uuid'])
#         price = activity['activity']['activity_informations']['price']

#         transaction_id = generate_transaction_id()

#         if price == 0:
#             is_free = True
#             status = 'Sukses'
#             metode = '-'
#         else:
#             is_free = False
#             status = 'Menunggu Pembayaran'
#             metode = 'Transfer Bank'
        
#         expired_at = timezone.now() + timezone.timedelta(minutes=10)

#         existing_transaction = Transaction.objects.filter(member=member, activity_id=activity_id).first()
        
#         try:
#             transaction = Transaction.objects.create(
#                 transaction_id=transaction_id,
#                 member=member,
#                 mitra=mitra,
#                 activity_id=activity_id,
#                 is_free=is_free,
#                 total_price=price,
#                 status=status,
#                 payment_method=metode,
#                 expired_at=expired_at                      
#             )        

#             return redirect('app.member:transactions')        
#         except:
#             return _500(request)