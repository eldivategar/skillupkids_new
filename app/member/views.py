from django.shortcuts import render, get_object_or_404
from app.helpers.decorators import cek_member_session
from app.helpers.utils import get_member_data
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from app.models import Member, Transaction, ActivityList, Testimonial
from app.activity.helpers import get_activity_detail, get_activity_list, get_category, get_activity_detail_by_name
from .helpers import get_all_transactions, get_transaction, get_member_activity, check_testimoni_member
from app.helpers.utils import redirect_to_whatsapp
from skillupkids import settings

@cek_member_session
def member_profile(request):
    data = get_member_data(request)
    return render(request, 'member/profile.html', {'data': data})

@cek_member_session
def member_profile_update(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        number = request.POST.get('num_wa')
        address = request.POST.get('address')
        email = request.POST.get('email')
        profile_image = request.FILES.get('profile_image')

        customer_id = request.session.get('customer_id')
        uuid = customer_id[2:]

        try:
            member = Member.objects.get(uuid=uuid)

        except Member.DoesNotExist:
            messages.error(request, 'Terjadi kesalahan saat update profile!')
            return redirect('app.member:member_profile')

        member.name = name
        member.number = number
        member.address = address
        member.email = email
        
        if profile_image:
            if member.profile_image.name != 'member/avatar-profile.jpg':
                member.profile_image.delete()

            member.profile_image.save(profile_image.name, profile_image, save=True)

        member.save()
        messages.success(request, 'Profile berhasil diupdate!')
        return redirect('app.member:member_profile')        
    else:
        return HttpResponse('Method not allowed!')

@cek_member_session
def member_profile_security(request):
    if request.method == 'GET':
        data = get_member_data(request)
        return render(request, 'member/security.html', {'data': data})

@cek_member_session
def member_profile_security_update(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        customer_id = request.session.get('customer_id')[2:]
        if password == confirm_password:
            try:
                member = Member.objects.get(uuid=customer_id)
                member.password = password
                member.save()
                messages.success(request, 'Password berhasil diupdate!')
                return redirect('app.member:member_profile_security')
            except Member.DoesNotExist:
                messages.error(request, 'Terjadi kesalahan saat update password!')
                return redirect('app.member:member_profile_security')
        else:
            messages.error(request, 'Password tidak sama!')
            return redirect('app.member:member_profile_security')
    else:
        return HttpResponse('Method not allowed!')

@cek_member_session
def transactions(request):
    data = get_member_data(request)
    member_id = request.session.get('customer_id')[2:]
    transactions = get_all_transactions(member_id)
        
    return render(request, 'member/transactions.html', {'data': data, 'transactions': transactions, 'client_key': settings.MIDTRANS_CLIENT_KEY, 'snap_js_url': settings.SNAP_JS_URL})

@cek_member_session
def chat_to_pay(request, transaction_id):
    if request.method == 'GET':
        customer_id = request.session.get('customer_id')[2:]
        member = Member.objects.get(uuid=customer_id)
        transactions = get_transaction(customer_id, transaction_id=transaction_id)
        activity_name = transactions[0]['activity']
        total_price = transactions[0]['total_price']
        invoice = transactions[0]['transaction_id']
        message = f'Halo admin %F0%9F%98%80 \nSaya atas nama *{member}* ingin melakukan pembayaran kegiatan. \nNama Kegiatan: *{activity_name}* \nTotal: *{total_price}* \nInvoice: *{invoice}*'
        return redirect_to_whatsapp(message)

@cek_member_session
def member_dashboard_activity(request):
    if request.method == 'GET':
        member_id = request.session.get('customer_id')[2:]
        category = request.GET.get('category')
        keyword = request.GET.get('keyword')        
            
        if category == None and keyword == None:
            list_of_activity = get_activity_list(category='all')

        elif category == None and keyword != None:
            list_of_activity = get_activity_list(keyword=keyword)
            
        elif category != None and keyword == None:
            list_of_activity = get_activity_list(category=category)
            
        elif category != None and keyword != None:
            list_of_activity = get_activity_list(category=category, keyword=keyword)                

        categories = get_category()
        activities = get_member_activity(member_id)

        data = get_member_data(request)
        return render(request, 'member/dashboard/activity.html', {'data': data, 'list_of_activity': list_of_activity, 'category': categories, 'activities': activities})

@cek_member_session
def view_activity(request, id, activity):
    if request.method == 'GET':
        member_id = request.session.get('customer_id')[2:]
        data = get_member_data(request)
        data_detail_activity = get_activity_detail(id)
        check_testimoni = check_testimoni_member(member_id, id)
        return render(request, 'member/dashboard/view-activity.html', {'data': data, 'data_detail_activity': data_detail_activity, 'check_testimoni': check_testimoni})

@cek_member_session
def rating(request, activity_id):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        testimoni = request.POST.get('testimoni')
        member_id = request.session.get('customer_id')[2:]
        member_id = Member.objects.get(uuid=member_id)
        activity = ActivityList.objects.get(activity_id=activity_id)
        
        
        Testimonial.objects.create(
            member=member_id,
            activity=activity,
            rating=rating,
            testimonial=testimoni
        )

        messages.success(request, 'Terima kasih atas penilaian anda!')        
        return redirect('app.member:view_activity', id=activity_id, activity=activity.activity_name)

@cek_member_session
def chat_to_admin(request):
    if request.method == 'GET':
        customer_id = request.session.get('customer_id')[2:]
        member = get_object_or_404(Member, uuid=customer_id)
        message = f'Halo admin %F0%9F%98%80 \nSaya atas nama *{member.name}* ingin bertanya tentang...'
        return redirect_to_whatsapp(message)