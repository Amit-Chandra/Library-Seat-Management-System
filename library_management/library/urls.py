from django.urls import path
from django.contrib import admin
from .api_views import StudentSignupAPI, StudentProfileAPI, LibraryListAPI, SeatAvailabilityAPI, ApproveStudentAPI
from .regular_views import student_signup, student_profile, library_list, seat_availability, approve_student
from . import regular_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # API Endpoints
    path('api/signup/', StudentSignupAPI.as_view(), name='student_signup_api'),
    path('api/profile/', StudentProfileAPI.as_view(), name='student_profile_api'),
    path('api/libraries/', LibraryListAPI.as_view(), name='library_list_api'),
    path('api/libraries/<int:library_id>/seats/', SeatAvailabilityAPI.as_view(), name='seat_availability_api'),
    path('api/approve_student/<int:student_id>/', ApproveStudentAPI.as_view(), name='approve_student_api'),

    # Regular Views
    path('', regular_views.home, name='home'),  # Home view
    path('signup/', regular_views.student_signup, name='student_signup'),  # Student signup
    path('profile/', regular_views.student_profile, name='student_profile'),  # Student profile
    path('libraries/', regular_views.library_list, name='library_list'),  # List libraries
    path('libraries/<int:library_id>/seats/', regular_views.seat_availability, name='seat_availability'),  # Seat availability
    path('approve_student/<int:student_id>/', regular_views.approve_student, name='approve_student'),  # Approve student
    path('admin_panel/', regular_views.admin_panel, name='admin_panel'),  # Admin panel for superusers
    path('admin/create/', regular_views.create_admin, name='create_admin'),  # Create admin
    path('admin/update/<int:admin_id>/', regular_views.update_admin, name='update_admin'),  # Update admin
    path('admin/delete/<int:admin_id>/', regular_views.delete_admin, name='delete_admin'),  # Delete admin


    # path('signup/', student_signup, name='student_signup'),
    # path('profile/', student_profile, name='student_profile'),
    # path('libraries/', regular_views.library_list, name='library_list'),
    # path('signup/', regular_views.student_signup, name='student_signup'),  
    # path('profile/', regular_views.student_profile, name='student_profile'),
    # path('libraries/<int:library_id>/seats/', regular_views.seat_availability, name='seat_availability'),
    # path('approve_student/<int:student_id>/', regular_views.approve_student, name='approve_student'),
    # path('libraries/', library_list, name='library_list'),
    # path('libraries/', regular_views.library_list, name='library_list'),
    # path('libraries/<int:library_id>/seats/', seat_availability, name='seat_availability'),
    # path('approve_student/<int:student_id>/', approve_student, name='approve_student'),
]
