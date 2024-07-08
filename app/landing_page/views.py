from django.shortcuts import render, redirect
from app.helpers.utils import get_member_data, get_mitra_data
from app.activity.helpers import get_category, get_new_activity, get_testimonial
from django.views.decorators.cache import cache_page
from app.models import Member, Mitra, ActivityList, Blog
from asgiref.sync import sync_to_async
from .helpers import get_achievements

# @cache_page(604800)
async def home(request):
    category = await sync_to_async(get_category)()
    new_activity = await sync_to_async(get_new_activity)(num=8)
    testimonials = await sync_to_async(get_testimonial)()
    achievements = await get_achievements(request)

    if 'customer_id' not in request.session:
        return await sync_to_async(render)(request, 'landing_page/index.html', {'category': category, 'new_activity': new_activity, 'testimonials': testimonials, 'achievements': achievements})
    else:
        customer = request.session.get('customer_id')
        if customer[:2] == 'mi' :
            data = await sync_to_async(get_mitra_data)(request)
        elif customer[:2] == 'me':
            data = await sync_to_async(get_member_data)(request)
    
    return await sync_to_async(render)(request, 'landing_page/index.html', {'data': data, 'category': category, 'new_activity': new_activity, 'testimonials': testimonials, 'achievements': achievements})

@cache_page(60*60*24)
def about(request):
    if request.method == 'GET':
        if 'customer_id' not in request.session:
            return render(request, 'landing_page/about.html')
        else:
            customer = request.session.get('customer_id')
            if customer[:2] == 'mi' :
                data = get_mitra_data(request)
            elif customer[:2] == 'me':
                data = get_member_data(request)
        
        return render(request, 'landing_page/about.html', {'data': data})

@cache_page(60*60*24)
def contact(request):
    if 'customer_id' not in request.session:
        return render(request, 'landing_page/contact.html')
    else:
        customer = request.session.get('customer_id')
        if customer[:2] == 'mi' :
            data = get_mitra_data(request)
        elif customer[:2] == 'me':
            data = get_member_data(request)
        
        return render(request, 'landing_page/contact.html', {'data': data})

@cache_page(60*60*6)
def blog(request):
    if request.method == 'GET':
        get_blogs = Blog.objects.all()
        
        if 'customer_id' not in request.session:
            return render(request, 'landing_page/blog.html', {'get_blogs': get_blogs})
        else:
            customer = request.session.get('customer_id')

            if customer[:2] == 'mi' :
                data = get_mitra_data(request)
            elif customer[:2] == 'me':
                data = get_member_data(request)
        return render(request, 'landing_page/blog.html', {'data': data, 'get_blogs': get_blogs})

@cache_page(60*60*6)
def blog_detail(request, blog_id, blog_title):
    if request.method == 'GET':
        get_blog = Blog.objects.get(blog_id=blog_id)
        
        if 'customer_id' not in request.session:
            return render(request, 'landing_page/blog_detail.html', {'get_blog': get_blog})
        else:
            customer = request.session.get('customer_id')

            if customer[:2] == 'mi' :
                data = get_mitra_data(request)
            elif customer[:2] == 'me':
                data = get_member_data(request)
        
        return render(request, 'landing_page/blog_detail.html', {'data': data, 'get_blog': get_blog})

@cache_page(60*60*6)
def terms_of_use(request):
    if 'customer_id' not in request.session:
        return render(request, 'landing_page/terms.html')
    else:
        customer = request.session.get('customer_id')
        if customer[:2] == 'mi' :
            data = get_mitra_data(request)
        elif customer[:2] == 'me':
            data = get_member_data(request)
        
        return render(request, 'landing_page/terms.html', {'data': data})