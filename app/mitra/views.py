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
        uuid = customer_id[2:]

        try:
            mitra = Mitra.objects.get(uuid=uuid)

        except Mitra.DoesNotExist:
            messages.error(request, 'Terjadi kesalahan saat update profile!')
            return redirect('app.mitra:mitra_profile')

        mitra.name = name
        mitra.number = number
        mitra.address = address
        mitra.email = email
        mitra.city = city
        mitra.description = description
        mitra.start_time = start_time
        mitra.end_time = end_time
        
        if profile_image:
            if mitra.profile_image.name != 'mitra/default-logo.png':
                mitra.profile_image.delete()
            mitra.profile_image.save(profile_image.name, profile_image, save=True)

        mitra.save()
        messages.success(request, 'Profile berhasil diupdate!')
        return redirect('app.mitra:mitra_profile')        
    else:
        return HttpResponse('Method not allowed!')

@cek_mitra_session
def mitra_sosmed(request):
    data = get_mitra_data(request)
    return render(request, 'mitra/sosmed.html', {'data': data})

@cek_mitra_session
def mitra_sosmed_update(request):
    if request.method == 'POST':
        twitter = request.POST.get('twitter_')
        fb = request.POST.get('fb_')
        ig = request.POST.get('ig_')
        linkedin = request.POST.get('linkedin_')
        yt = request.POST.get('yt_')

        customer_id = request.session.get('customer_id')
        uuid = customer_id[2:]

        try:
            mitra = Mitra.objects.get(uuid=uuid)

        except Mitra.DoesNotExist:
            messages.error(request, 'Terjadi kesalahan saat update profile!')
            return redirect('app.mitra:mitra_sosmed')

        mitra.twitter_site = twitter
        mitra.fb_site = fb
        mitra.ig_site = ig
        mitra.linkedin_site = linkedin
        mitra.yt_site = yt

        mitra.save()
        messages.success(request, 'Profile berhasil diupdate!')
        return redirect('app.mitra:mitra_sosmed')        
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