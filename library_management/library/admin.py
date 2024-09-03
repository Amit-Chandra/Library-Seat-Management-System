# library_management/library/admin.py

from django.contrib import admin
from .models import Library, Seat, UserProfile, Payment

admin.site.register(Library)
admin.site.register(Seat)
admin.site.register(UserProfile)
admin.site.register(Payment)






# from django.contrib import admin
# from .models import Library, Seat, UserProfile, Payment

# admin.site.register(Library)
# admin.site.register(Seat)
# admin.site.register(UserProfile)
# admin.site.register(Payment)
