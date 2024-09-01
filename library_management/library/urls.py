from django.urls import path
from .views import student_signup, library_list, seat_availability, student_profile, approve_student
from django.contrib import admin
from django.urls import path, include
from django.urls import path
from .views import (
    StudentSignupAPI,
    LibraryListAPI,
    SeatAvailabilityAPI,
    StudentProfileAPI,
    ApproveStudentAPI
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('library/', include('library.urls')),
    path('api/signup/', StudentSignupAPI.as_view(), name='student_signup'),
    path('api/libraries/', LibraryListAPI.as_view(), name='library_list'),
    path('api/libraries/<int:library_id>/seats/', SeatAvailabilityAPI.as_view(), name='seat_availability'),
    path('api/profile/', StudentProfileAPI.as_view(), name='student_profile'),
    path('api/approve_student/<int:student_id>/', ApproveStudentAPI.as_view(), name='approve_student'),
]









# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('library/', include('library.urls')),
#     path('signup/', student_signup, name='student_signup'),
#     path('libraries/', library_list, name='library_list'),
#     path('libraries/<int:library_id>/seats/', seat_availability, name='seat_availability'),
#     path('profile/', student_profile, name='student_profile'),
#     path('approve_student/<int:student_id>/', approve_student, name='approve_student'),
# ]
