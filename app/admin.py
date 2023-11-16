from django.contrib import admin
from .models import Member, Mitra, ActivityList, Testimonial, Transaction

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'member', 'mitra', 'activity', 'date', 'status', 'total_price', 'payment_method', 'expired_at')
    list_filter = ('status', 'date','payment_method', 'is_free')
    ordering = ('-date',)

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('activity_id', 'activity_name', 'mitra_activity', 'category', 'activity_status')
    list_filter = ('mitra_activity', 'activity_status', 'category')
    

# Register your models here.
admin.site.register(Member)
admin.site.register(Mitra)
admin.site.register(ActivityList, ActivityAdmin)
admin.site.register(Testimonial)
admin.site.register(Transaction, TransactionAdmin)
