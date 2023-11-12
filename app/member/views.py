from django.shortcuts import render
from app.helpers.decorators import cek_member_session
from app.helpers.utils import get_member_data
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse
from app.models import Member
from app.activity.helpers import get_activity_detail, get_activity_list, get_category
from .helpers import get_transactions
from app.helpers.utils import redirect_to_whatsapp

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
    transactions = get_transactions(member_id)
        
    return render(request, 'member/transactions.html', {'data': data, 'transactions': transactions})

@cek_member_session
def chat_to_pay(request, id):
    if request.method == 'GET':
        customer_id = request.session.get('customer_id')[2:]
        member = Member.objects.get(uuid=customer_id)
        transactions = get_transactions(customer_id)
        activity_name = transactions[0]['activity']['activity_name']
        total_price = transactions[0]['transaction']['total_price']
        message = f'Halo admin %F0%9F%98%80 \nSaya atas nama *{member}* ingin melakukan pembayaran kegiatan *{activity_name}* sebesar *{total_price}*!'
        return redirect_to_whatsapp(message)

@cek_member_session
def member_dashboard_activity(request):
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

    data = get_member_data(request)
    return render(request, 'member/dashboard/activity.html', {'data': data, 'list_of_activity': list_of_activity, 'category': categories})