from django.urls import path
from .api_views import StudentSignupAPI, StudentProfileAPI, LibraryListAPI, SeatAvailabilityAPI, ApproveStudentAPI
from .regular_views import student_signup, student_profile, library_list, seat_availability, approve_student

urlpatterns = [
    # API Endpoints
    path('api/signup/', StudentSignupAPI.as_view(), name='student_signup_api'),
    path('api/profile/', StudentProfileAPI.as_view(), name='student_profile_api'),
    path('api/libraries/', LibraryListAPI.as_view(), name='library_list_api'),
    path('api/libraries/<int:library_id>/seats/', SeatAvailabilityAPI.as_view(), name='seat_availability_api'),
    path('api/approve_student/<int:student_id>/', ApproveStudentAPI.as_view(), name='approve_student_api'),

    # Regular Views
    path('signup/', student_signup, name='student_signup'),
    path('profile/', student_profile, name='student_profile'),
    path('libraries/', library_list, name='library_list'),
    path('libraries/<int:library_id>/seats/', seat_availability, name='seat_availability'),
    path('approve_student/<int:student_id>/', approve_student, name='approve_student'),
]
