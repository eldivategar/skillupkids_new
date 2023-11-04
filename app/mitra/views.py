from django.shortcuts import render
from app.helpers.decorators import cek_mitra_session
from app.helpers.utils import get_mitra_data
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse
from app.models import Mitra


@cek_mitra_session
def mitra_profile(request):
    data = get_mitra_data(request)
    return render(request, 'mitra/profile.html', {'data': data})

@cek_mitra_session
def mitra_profile_update(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        number = request.POST.get('num_wa')
        address = request.POST.get('address')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        description = request.POST.get('description')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        profile_image = request.FILES.get('profile_image')

        customer_id = request.session.get('customer_id')

        try:
            customer = Mitra.objects.get(uuid=customer_id)

        except Mitra.DoesNotExist:
            messages.error(request, 'Terjadi kesalahan saat update profile!')
            return redirect('app.mitra:mitra_profile')

        customer.name = name
        customer.number = number
        customer.address = address
        customer.email = email
        customer.city = city
        customer.description = description
        customer.start_time = start_time
        customer.end_time = end_time
        
        if profile_image:            
            customer.profile_image.delete()
            customer.profile_image.save(profile_image.name, profile_image, save=True)

        customer.save()
        messages.success(request, 'Profile berhasil diupdate!')
        return redirect('app.mitra:mitra_profile')        
    else:
        return HttpResponse('Method not allowed!')

@cek_mitra_session
def mitra_profile_security(request):
    if request.method == 'GET':
        data = get_mitra_data(request)
        return render(request, 'mitra/security.html', {'data': data})

@cek_mitra_session
def mitra_dashboard_activity(request):
    data = get_mitra_data(request)
    return render(request, 'mitra/dashboard/activity.html', {'data': data})