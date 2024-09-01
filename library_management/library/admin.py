from django.contrib import admin
from .models import Library, Seat, UserProfile, Payment

admin.site.register(Library)
admin.site.register(Seat)
admin.site.register(UserProfile)
admin.site.register(Payment)
