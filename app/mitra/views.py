from django.shortcuts import render
from app.helpers.decorators import cek_mitra_session
from app.helpers.utils import get_mitra_data
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse
from app.models import Mitra, ActivityList


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
def mitra_dashboard_activity_list(request):
    mitra_id = request.session.get('customer_id')[2:]
    data = get_mitra_data(request)
    all_activity = ActivityList.objects.filter(mitra_activity=mitra_id).order_by('-activity_id')
    
    data_activity = [row.activity_json() for row in all_activity]
    print(data_activity)
    return render(request, 'mitra/dashboard/list-of-activity.html', {'data': data, 'data_activity': data_activity})

@cek_mitra_session
def mitra_create_new_activity(request):
    if request.method == 'GET':
        data = get_mitra_data(request)
        return render(request, 'mitra/dashboard/create-new-activity.html', {'data': data})
    
    if request.method == 'POST':
        mitra_id = request.session.get('customer_id')[2:]

        # Basic Information
        activity_name = request.POST.get('activity_name')
        sub_description = request.POST.get('sub_description')
        category = request.POST.get('category')
        if category == 'other':
            category = request.POST.get('custom_category')

        # Activity Information
        day = request.POST.get('day')
        price = float(request.POST.get('price').replace(',', ''))
        duration = request.POST.get('duration')
        age = request.POST.get('age')
        learning_method = request.POST.get('learning_method')
        description = request.POST.get('description')

        # Media
        image = request.FILES.get('cover_image')  

        # Additional Information
        requirements = request.POST.get('requirements')
        benefit = request.POST.get('benefit')
        additional_information = request.POST.get('additional_information')

        try:
            mitra = Mitra.objects.get(uuid=mitra_id)
            activity = ActivityList.objects.create(
                mitra_activity=mitra,
                activity_name=activity_name,
                category=category,
                day=day,
                price=price,
                duration=duration,
                age=age,
                learning_method=learning_method,
                sub_description=sub_description,
                description=description,
                requirements=requirements,
                benefit=benefit,
                additional_information=additional_information,
            )
            if image:
                activity.activity_image.save(image.name, image, save=True)
            messages.success(request, 'Aktivitas berhasil dibuat!')
            return redirect('app.mitra:mitra_dashboard_activity_list')
        
        except Mitra.DoesNotExist:
            messages.error(request, 'Terjadi kesalahan saat membuat aktivitas baru!')
            return redirect('app.mitra:mitra_dashboard_activity_list')