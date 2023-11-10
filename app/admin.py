from django.contrib import admin
from .models import Member, Mitra, ActivityList, Testimonial, Transaction

# Register your models here.
admin.site.register(Member)
admin.site.register(Mitra)
admin.site.register(ActivityList)
admin.site.register(Testimonial)
admin.site.register(Transaction)