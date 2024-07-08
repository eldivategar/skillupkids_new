from django.contrib import admin
from django import forms
from .models import Member, Mitra, ActivityList, Testimonial, Transaction, Blog, FeaturedActivity

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'member', 'mitra', 'activity', 'date', 'status', 'total_price', 'payment_method', 'expired_at')
    list_filter = ('status', 'date','payment_method', 'is_free')
    ordering = ('-date',)

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('activity_name', 'price', 'mitra_activity', 'category', 'activity_status')
    list_filter = ('mitra_activity', 'activity_status', 'category')
    search_fields = ('activity_name', 'category')
    
    
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
    
class FeaturedActivityForm(forms.ModelForm):
    class Meta:
        model = FeaturedActivity
        fields = ['activity']

    def __init__(self, *args, **kwargs):
        super(FeaturedActivityForm, self).__init__(*args, **kwargs)
        self.fields['activity'].queryset = ActivityList.objects.all()
        self.fields['activity'].label_from_instance = lambda obj: obj.full_activity_name()

class FeaturedActivityAdmin(admin.ModelAdmin):
    form = FeaturedActivityForm
    list_display = ('get_activity_name', 'get_mitra_name')

    def get_activity_name(self, obj):
        return obj.activity.activity_name
    get_activity_name.short_description = 'Activity Name'

    def get_mitra_name(self, obj):
        return obj.activity.mitra_activity.name
    get_mitra_name.short_description = 'Mitra Name'

# Register your models here.
admin.site.register(Member, MemberAdmin)
admin.site.register(Mitra, MitraAdmin)
admin.site.register(ActivityList, ActivityAdmin)
admin.site.register(Testimonial, TestimoniAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(FeaturedActivity, FeaturedActivityAdmin)
