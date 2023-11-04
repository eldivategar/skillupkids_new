from django.shortcuts import render
from app.helpers.decorators import cek_member_session
from app.helpers.utils import get_member_data
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse
from app.models import Member


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

        try:
            customer = Member.objects.get(uuid=customer_id)

        except Member.DoesNotExist:
            messages.error(request, 'Terjadi kesalahan saat update profile!')
            return redirect('app.member:member_profile')

        customer.name = name
        customer.number = number
        customer.address = address
        customer.email = email
        
        if profile_image:
            if customer.profile_image.name != 'member/avatar-profile.jpg':
                customer.profile_image.delete()

            customer.profile_image.save(profile_image.name, profile_image, save=True)

        customer.save()
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
def member_dashboard_activity(request):
    data = get_member_data(request)
    return render(request, 'member/dashboard/activity.html', {'data': data})