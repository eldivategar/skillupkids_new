from django.contrib import admin
from .models import Member, Mitra, ActivityList, Testimonial, Transaction, Blog

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'member', 'mitra', 'activity', 'date', 'status', 'total_price', 'payment_method', 'expired_at')
    list_filter = ('status', 'date','payment_method', 'is_free')
    ordering = ('-date',)

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('activity_name', 'price', 'mitra_activity', 'category', 'activity_status')
    list_filter = ('mitra_activity', 'activity_status', 'category')
    
    
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'number', 'address')
    # list_filter = ('city')
    
    
class MitraAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'number', 'address')
    # list_filter = ('city')

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'tag')
    list_filter = ('created_at', 'tag')    
    
class TestimoniAdmin(admin.ModelAdmin):
    list_display = ('member', 'activity', 'testimonial', 'date')
    list_filter = ('date',)
    

# Register your models here.
admin.site.register(Member, MemberAdmin)
admin.site.register(Mitra, MitraAdmin)
admin.site.register(ActivityList, ActivityAdmin)
admin.site.register(Testimonial, TestimoniAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Blog, BlogAdmin)
