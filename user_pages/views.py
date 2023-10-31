from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from main_platform.helpers.decorators import cek_user_session
from main_platform.helpers.utils import get_customer_data
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse
from .models import Member

@cek_user_session
def member_activity(request):
    data = get_customer_data(request)
    return render(request, 'member/activity.html', {'data': data})

@cek_user_session
def member_profile(request):
    data = get_customer_data(request)
    return render(request, 'member/profile.html', {'data': data})

@cek_user_session
def member_profile_update(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        number = request.POST.get('num_wa')
        address = request.POST.get('address')
        email = request.POST.get('email')

        if name and number and address and email:
            customer_id = request.session.get('customer_id')

            try:
                customer = Member.objects.get(uuid=customer_id)
            except Member.DoesNotExist:
                messages.error(request, 'Terjadi kesalahan saat update profile!')
                return redirect('user_pages:member_profile')

            customer.name = name
            customer.number = number
            customer.address = address
            customer.email = email

            customer.save()
            messages.success(request, 'Profile berhasil diupdate!')
            return redirect('user_pages:member_profile')
        else:
            return HttpResponse('Please fill all the fields!')
    else:
        return HttpResponse('Method not allowed!')


        